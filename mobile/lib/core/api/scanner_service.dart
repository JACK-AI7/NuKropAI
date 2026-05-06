import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'dart:convert';
import 'local_database.dart';
import '../ai/on_device_ai_service.dart';
import '../ai/llm_service.dart';
import 'cloud_ai_service.dart';
import 'package:flutter_tts/flutter_tts.dart';
import '../constants/app_constants.dart';

final currentWeatherProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final service = ScannerService();
  return await service.getCurrentWeather();
});

final scannerServiceProvider = Provider((ref) => ScannerService());

class ScannerService {
  ScannerService();
  final OnDeviceAIService _onDeviceAI = OnDeviceAIService();
  final LLMService _llmService = LLMService();
  final CloudAIService _cloudAI = CloudAIService();
  final FlutterTts _tts = FlutterTts();
  String? regionHint;

  Future<void> init() async {
    await _onDeviceAI.loadModel();
    await _llmService.init();
  }

  /// Fetch real-time weather directly from Open-Meteo (no API key needed)
  Future<Map<String, dynamic>> getCurrentWeather() async {
    final position = await _getCurrentLocation();
    if (position == null) {
      return {
        'temp': '--',
        'condition': 'Location Disabled',
        'location': 'Unknown',
        'humidity': '--',
        'windSpeed': '--',
        'icon': Icons.location_off,
      };
    }

    final lat = position.latitude;
    final lng = position.longitude;
    
    String locationName = '${lat.toStringAsFixed(2)}°N, ${lng.toStringAsFixed(2)}°E';
    try {
      List<Placemark> placemarks = await placemarkFromCoordinates(lat, lng);
      if (placemarks.isNotEmpty) {
        final place = placemarks.first;
        locationName = '${place.locality ?? place.subAdministrativeArea ?? ''}, ${place.administrativeArea ?? ''}';
      }
    } catch (e) {
      debugPrint('Geocoding error: $e');
    }

    try {
      final url = 'https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lng&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m';
      final response = await Dio().get(url);
      final data = response.data['current'];

      return {
        'temp': data['temperature_2m'].round(),
        'condition': _getWeatherCondition(data['weather_code']),
        'location': locationName,
        'humidity': data['relative_humidity_2m'],
        'windSpeed': data['wind_speed_10m'],
        'icon': _getWeatherIcon(data['weather_code']),
      };
    } catch (e) {
      debugPrint('Weather fetch error: $e');
      return {
        'temp': '--',
        'condition': 'Unavailable',
        'location': locationName,
        'humidity': '--',
        'windSpeed': '--',
        'icon': Icons.location_off,
      };
    }
  }

  IconData _getWeatherIcon(int? code) {
    if (code == null) return Icons.cloud;
    if (code == 0) return Icons.wb_sunny;
    if (code >= 1 && code <= 3) return Icons.wb_cloudy;
    if (code >= 45 && code <= 48) return Icons.foggy;
    if (code >= 51 && code <= 67) return Icons.grain;
    if (code >= 71 && code <= 77) return Icons.ac_unit;
    if (code >= 80 && code <= 82) return Icons.umbrella;
    if (code >= 95 && code <= 99) return Icons.bolt;
    return Icons.cloud;
  }

  String _getWeatherCondition(int? code) {
    if (code == null) return 'Unknown';
    if (code == 0) return 'Clear Sky';
    if (code >= 1 && code <= 3) return 'Partly Cloudy';
    if (code >= 45 && code <= 48) return 'Foggy';
    if (code >= 51 && code <= 67) return 'Rain';
    if (code >= 71 && code <= 77) return 'Snow';
    if (code >= 80 && code <= 82) return 'Showers';
    if (code >= 95 && code <= 99) return 'Thunderstorm';
    return 'Cloudy';
  }

  Future<void> speakResult(String text, {String lang = 'en-US'}) async {
    await _tts.setLanguage(lang);
    await _tts.setPitch(1.0);
    await _tts.speak(text);
  }

  Future<Map<String, dynamic>> getSatelliteAnalysis() async {
    final pos = await _getCurrentLocation();
    if (pos == null) throw Exception("Location required for satellite analysis");
    
    final response = await Dio().get(
      '${AppConstants.aiServerUrl}/analyze/satellite',
      queryParameters: {'lat': pos.latitude, 'lon': pos.longitude},
      options: Options(headers: {'X-API-Key': 'nukrop_secret_dev'}),
    );
    return response.data;
  }

  Future<Map<String, dynamic>> getForecast() async {
    final pos = await _getCurrentLocation();
    if (pos == null) throw Exception("Location required for forecast");
    
    final response = await Dio().get(
      '${AppConstants.aiServerUrl}/analytics/forecast',
      queryParameters: {'lat': pos.latitude, 'lon': pos.longitude},
      options: Options(headers: {'X-API-Key': 'nukrop_secret_dev'}),
    );
    return response.data;
  }

  /// Main scan function — performs on-device analysis and optionally cloud LLM
  Future<Map<String, dynamic>> scanImage(XFile image, {bool isSoil = false}) async {
    final position = await _getCurrentLocation();
    final lat = position?.latitude;
    final lng = position?.longitude;

    // 1. Fetch weather concurrently
    final weather = await getCurrentWeather();

    // 2. On-device TFLite analysis (fast, offline)
    final onDeviceResult = await _onDeviceAI.analyzeImage(image.path, isSoil: isSoil);
    if (onDeviceResult == null) {
      throw Exception('On-device AI model not loaded or analysis failed');
    }

    // 2.5 Cloud specialized analysis (Hugging Face)
    List<Map<String, dynamic>> cloudDetections = [];
    Map<String, dynamic> cloudCropResult = {};
    if (!isSoil) {
      try {
        // Run specialized detection via HF Router
        cloudCropResult = await _cloudAI.analyzeCrop(image.path);
        
        // Use results from HF if confidence is high
        if (cloudCropResult['classification'] != null) {
           final cls = cloudCropResult['classification'];
           if ((cls['confidence'] as num) > (onDeviceResult['confidence'] as num)) {
             onDeviceResult['diseaseName'] = cls['label'];
             onDeviceResult['confidence'] = cls['confidence'];
           }
        }
        
        // Merge detections if any
        if (cloudCropResult['detections'] != null) {
          cloudDetections = List<Map<String, dynamic>>.from(cloudCropResult['detections']);
        }
      } catch (e) {
        debugPrint('Cloud crop analysis failed: $e');
      }
    } else {
       try {
         final soilResult = await _cloudAI.classifySoil(image.path);
         if (soilResult['soil_type'] != null) {
           onDeviceResult['soilType'] = soilResult['soil_type'];
           onDeviceResult['confidence'] = soilResult['confidence'];
         }
       } catch (e) {
         debugPrint('Cloud soil classification failed: $e');
       }
    }

    // 2.7 Advanced Multimodal Analysis (if online and not soil)
    Map<String, dynamic> advancedResult = {};
    if (!isSoil) {
      try {
        advancedResult = await _cloudAI.analyzeAdvanced(image.path);
      } catch (e) {
        debugPrint('Advanced multimodal analysis failed: $e');
      }
    }

    // 3. Cloud Analysis via HF SpaceLLaVA (if online)
    String? treatment;
    String? fertilizer;
    String? pesticide;
    String? prevention;
    String? chemicalClass;
    String? aiSource;

    try {
      // Use the advanced analysis from HF SpaceLLaVA
      final response = await _cloudAI.analyzeAdvanced(image.path);
      if (response['response'] != null && response['response'].isNotEmpty) {
        final llmResponse = response['response'];
        // Parse the LLM response (SpaceLLaVA usually returns text, but we try to parse JSON if it exists)
        final parsed = _parseLLMResponse(llmResponse, isSoil);
        
        treatment = parsed['treatment'] ?? llmResponse;
        fertilizer = parsed['fertilizer'];
        pesticide = parsed['pesticide'];
        prevention = parsed['prevention'];
        chemicalClass = parsed['chemicalClass'];
        aiSource = 'hugging_face_mllm';
      } else {
        throw Exception('HF MLLM response empty');
      }
    } catch (e) {
      debugPrint('Cloud HF analysis failed, using on-device only: $e');
      aiSource = 'on_device';
      treatment = onDeviceResult['treatment'] ?? '';
      fertilizer = onDeviceResult['fertilizer'] ?? '';
      pesticide = onDeviceResult['pesticide'];
      prevention = onDeviceResult['prevention'];
      chemicalClass = onDeviceResult['chemicalClass'];
    }

    // 4. Determine region hint
    if (lat != null && lng != null) {
      regionHint = _getRegionHint(lat, lng);
    }

    // 5. Build final result
    final plantName = isSoil ? 'Soil' : (onDeviceResult['plantName'] ?? 'Unknown');
    final diseaseName = isSoil ? 'N/A' : (onDeviceResult['diseaseName'] ?? 'Unknown');
    final severity = onDeviceResult['severity'] ?? (isSoil ? 'Low' : 'Medium');
    final confidence = onDeviceResult['confidence'] ?? 0.5;
    final soilType = isSoil ? (onDeviceResult['soilType'] ?? 'Unknown') : null;
    final soilHealth = isSoil ? (onDeviceResult['soilHealth'] ?? 'Unknown') : null;
    final suitableCrops = isSoil ? (onDeviceResult['suitableCrops'] ?? []) : null;
    final npk = onDeviceResult['npk'] ?? onDeviceResult['fertilizer_npk'];

    // 6. Generate product research using HF MLLM (if online)
    Map<String, dynamic>? productResearch;
    String? productResearchSource;
    try {
      final researchResponse = await _cloudAI.chatWithAgronomist("Suggest products for $diseaseName on $plantName. Return as JSON suggestions.");
      final parsed = _parseProductResearch(researchResponse);
      if (parsed != null) {
        productResearch = parsed;
        productResearchSource = 'hugging_face';
      } else {
        throw Exception('HF product research failed');
      }
    } catch (e) {
      debugPrint('Product research failed: $e');
      // Fallback to on-device product suggestions if available
      final onDeviceProducts = onDeviceResult['productResearch'];
      if (onDeviceProducts != null) {
        try {
          productResearch = Map<String, dynamic>.from(onDeviceProducts as Map);
          productResearchSource = 'on_device';
        } catch (_) {}
      }
    }

    // 7. Construct full result
    final result = <String, dynamic>{
      'imageUrl': 'local://scan_${DateTime.now().millisecondsSinceEpoch}',
      'createdAt': DateTime.now().toIso8601String(),
      'isSoilAnalysis': isSoil,
      'aiSource': aiSource,
      'userId': FirebaseAuth.instance.currentUser?.uid ?? 'local_user',
      // Core fields
      'plantName': plantName,
      'diseaseName': diseaseName,
       'cause': onDeviceResult['cause'] ?? onDeviceResult['type'],
      'severity': severity,
      'confidence': confidence,
      'treatment': treatment,
      'fertilizer': fertilizer,
      'pesticide': pesticide,
      'soilType': soilType,
      'soilHealth': soilHealth,
      'latitude': lat,
      'longitude': lng,
      'weather': weather,
      'regionHint': regionHint,
      'npk': npk,
      'prevention': prevention,
      'chemicalClass': chemicalClass,
      'suitableCrops': suitableCrops,
      'matchedDiseaseKey': null,
      // Product research
      'productResearch': productResearch,
      'productResearchSource': productResearchSource,
      'productResearchError': productResearch == null ? 'LLM research failed' : null,
    };

    // 8. Save locally (sanitize first)
    final storageResult = _sanitizeForStorage(result);
    await LocalDatabase.saveScan(storageResult);

    // 9. Optionally sync to cloud if logged in
    if (FirebaseAuth.instance.currentUser != null) {
      try {
        await FirebaseFirestore.instance.collection('scans').add({
          ...storageResult,
          "userId": FirebaseAuth.instance.currentUser!.uid,
          "timestamp": FieldValue.serverTimestamp(),
        });
      } catch (e) {
        debugPrint('Cloud sync failed: $e');
      }
    }

    return result;
  }

  /// Remove non-serializable objects (like IconData) before JSON storage or Firestore
  Map<String, dynamic> _sanitizeForStorage(Map<String, dynamic> data) {
    final sanitized = Map<String, dynamic>.from(data);
    
    // Sanitize weather map: remove IconData, keep only primitives
    if (sanitized['weather'] != null) {
      try {
        final weatherMap = Map<String, dynamic>.from(sanitized['weather']);
        weatherMap.remove('icon'); // IconData not serializable
        sanitized['weather'] = weatherMap;
      } catch (_) {
        sanitized['weather'] = null;
      }
    }

    // Sanitize npk if it's a List (should be fine, but ensure it's List<num> not something else)
    if (sanitized['npk'] != null && sanitized['npk'] is List) {
      // ensure all elements are numbers
      final list = List<dynamic>.from(sanitized['npk']);
      sanitized['npk'] = list.map((e) => num.tryParse(e.toString()) ?? e).toList();
    }

    return sanitized;
  }

  String _buildAnalysisPrompt(Map<String, dynamic> onDevice, bool isSoil, Map<String, dynamic> weather) {
    if (isSoil) {
      return '''
You are an expert agronomist for Indian farmers. Analyze the soil image and preliminary data.

Preliminary analysis:
- Soil type: ${onDevice['soilType'] ?? 'Unknown'}
- Soil health: ${onDevice['soilHealth'] ?? 'Unknown'}
- Suggested nutrients: ${onDevice['nutrients'] ?? onDevice['fertilizer'] ?? 'Not specified'}

Current conditions: ${weather['temp']}°C, humidity ${weather['humidity']}%, condition: ${weather['condition']}.

RESPOND WITH ONLY VALID JSON (no markdown, no extra text):
{
  "treatment": "Detailed soil treatment steps",
  "fertilizer": "Specific NPK recommendations with Indian product names and quantities",
  "pesticide": null,
  "prevention": "Long-term soil health and fertility practices",
  "chemicalClass": "Soil Amendment"
}
''';
    } else {
      return '''
You are a crop disease specialist for Indian farmers. Analyze the plant image and preliminary diagnosis.

Preliminary analysis:
- Plant: ${onDevice['plantName'] ?? 'Unknown'}
- Problem: ${onDevice['diseaseName'] ?? 'Unknown'}
- Type: ${onDevice['type'] ?? 'Unknown'}
- Cause: ${onDevice['cause'] ?? onDevice['type'] ?? 'Unknown'}

Current conditions: ${weather['temp']}°C, humidity ${weather['humidity']}%, condition: ${weather['condition']}.

RESPOND WITH ONLY VALID JSON (no markdown, no extra text):
{
  "treatment": "Detailed treatment steps with application method and timing",
  "fertilizer": "NPK recommendations with Indian fertilizer brand names and dosages",
  "pesticide": "Active ingredient, formulation type, dosage per litre, and PHI",
  "prevention": "Cultural and preventive measures to avoid recurrence",
  "chemicalClass": "Fungicide or Insecticide or Herbicide or Other"
}
''';
    }
  }

  Map<String, String?> _parseLLMResponse(String response, bool isSoil) {
    try {
      // Clean response: remove markdown code blocks
      String cleaned = response.trim();
      cleaned = cleaned.replaceAll('```json', '').replaceAll('```json\n', '');
      cleaned = cleaned.replaceAll('```', '').replaceAll('```\n', '');
      cleaned = cleaned.trim();

      // Extract JSON object
      final start = cleaned.indexOf('{');
      final end = cleaned.lastIndexOf('}');
      if (start != -1 && end != -1 && end > start) {
        final jsonStr = cleaned.substring(start, end + 1);
        final Map<String, dynamic> parsed = jsonDecode(jsonStr);
        return {
          'treatment': parsed['treatment']?.toString(),
          'fertilizer': parsed['fertilizer']?.toString(),
          'pesticide': parsed['pesticide']?.toString(),
          'prevention': parsed['prevention']?.toString(),
          'chemicalClass': parsed['chemicalClass']?.toString(),
        };
      }

      // Fallback: try to parse line-by-line if JSON not found
      final lines = cleaned.split('\n');
      final result = <String, String?>{};
      for (final line in lines) {
        if (line.contains('treatment') || line.contains('Treatment')) {
          result['treatment'] = line.split(':').skip(1).join(':').trim();
        } else if (line.contains('fertilizer') || line.contains('Fertilizer')) {
          result['fertilizer'] = line.split(':').skip(1).join(':').trim();
        } else if (line.contains('pesticide') || line.contains('Pesticide')) {
          result['pesticide'] = line.split(':').skip(1).join(':').trim();
        } else if (line.contains('prevention') || line.contains('Prevention')) {
          result['prevention'] = line.split(':').skip(1).join(':').trim();
        } else if (line.contains('chemicalClass') || line.contains('class')) {
          result['chemicalClass'] = line.split(':').skip(1).join(':').trim();
        }
      }
      if (result.isNotEmpty) return result;
    } catch (e) {
      debugPrint('Failed to parse LLM response: $e');
    }
    return {};
  }

  String _buildProductResearchPrompt({
    required bool isSoil,
    required String plantName,
    required String diseaseName,
    String? treatment,
    String? pesticide,
    String? fertilizer,
    String? soilType,
    String? soilHealth,
    required Map<String, dynamic> weather,
    String? regionHint,
  }) {
    final region = regionHint ?? 'India (regional availability unknown)';
    if (isSoil) {
      return '''
You are an agricultural inputs advisor for India. A soil assessment was completed.

Soil details:
- Type: $soilType
- Health: $soilHealth
- Fertilizer plan: $fertilizer
- Region: $region
- Weather: ${weather['temp']}°C, ${weather['humidity']}% humidity

Suggest 3–5 specific fertilizer or soil amendment products available in this region.
Return ONLY valid JSON array (no markdown, no intro text):
[
  {
    "productName": "Specific product name",
    "productType": "Fertilizer|Soil amendment|Organic|Micronutrient",
    "activeIngredient": "Nutrient composition or active ingredient",
    "whyItFits": "Why this product suits this soil and region",
    "applicationTip": "How and when to apply",
    "safetyNote": "Important safety considerations",
    "purchaseUrl": "Search URL on Amazon.in or AgriBegri"
  }
]
''';
    } else {
      return '''
You are an agricultural inputs advisor for India. A crop problem was identified:

Crop: $plantName
Problem: $diseaseName
Treatment plan: $treatment
Pesticide guidance: $pesticide
Region: $region
Weather: ${weather['temp']}°C, ${weather['humidity']}% humidity

Suggest 3–5 specific pesticide/fungicide/bio-control products for this problem, commonly available in this region.
Return ONLY valid JSON array (no markdown, no intro text):
[
  {
    "productName": "Specific product name",
    "productType": "Fungicide|Insecticide|Bio-pesticide|Herbicide",
    "activeIngredient": "Active ingredient and concentration",
    "whyItFits": "Why this product is suitable",
    "applicationTip": "How to apply (dosage, timing)",
    "safetyNote": "PPE, PHI, resistance management",
    "purchaseUrl": "Search URL on Amazon.in or AgriBegri"
  }
]
''';
    }
  }

  Map<String, dynamic>? _parseProductResearch(String response) {
    try {
      String cleaned = response.trim();
      cleaned = cleaned.replaceAll('```json', '').replaceAll('```', '').trim();

      // Try to find JSON array
      final startArray = cleaned.indexOf('[');
      final endArray = cleaned.lastIndexOf(']');
      if (startArray != -1 && endArray != -1 && endArray > startArray) {
        final jsonStr = cleaned.substring(startArray, endArray + 1);
        final List<dynamic> list = jsonDecode(jsonStr);
        return {'suggestions': list, 'researchSummary': 'AI-generated product recommendations'};
      }

      // Try to find JSON object with suggestions key
      final startObj = cleaned.indexOf('{');
      final endObj = cleaned.lastIndexOf('}');
      if (startObj != -1 && endObj != -1 && endObj > startObj) {
        final jsonStr = cleaned.substring(startObj, endObj + 1);
        final Map<String, dynamic> parsed = jsonDecode(jsonStr);
        if (parsed.containsKey('suggestions')) {
          return parsed;
        }
      }
    } catch (e) {
      debugPrint('Failed to parse product research: $e');
    }
    return null;
  }

  String _getRegionHint(double lat, double lng) {
    if (lat > 28) return 'Northern India (Punjab, Haryana, UP)';
    if (lat < 15) return 'Southern India (TN, Karnataka, Kerala)';
    if (lng < 75) return 'Western India (Gujarat, Maharashtra)';
    if (lng > 85) return 'Eastern India (WB, Odisha, Bihar)';
    return 'Central India (MP, Chhattisgarh)';
  }

  Future<Position?> _getCurrentLocation() async {
    try {
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) return null;
      }
      if (permission == LocationPermission.deniedForever) return null;
      return await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.best,
        timeLimit: const Duration(seconds: 15),
      );
    } catch (e) {
      debugPrint('Location error: $e');
      return null;
    }
  }
}
