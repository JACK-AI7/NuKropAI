import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import 'package:geolocator/geolocator.dart';
import 'package:geocoding/geocoding.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import 'local_database.dart';
import 'api_client.dart';
import 'connectivity_service.dart';
import '../ai/on_device_ai_service.dart';

final currentWeatherProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final service = ScannerService();
  return await service.getCurrentWeather();
});

final scannerServiceProvider = Provider((ref) => ScannerService());

class ScannerService {
  ScannerService();
  final OnDeviceAIService _onDeviceAI = OnDeviceAIService();

  Future<void> init() async {
    await _onDeviceAI.loadModel();
  }

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
      // Direct call to Open-Meteo (Free, no key required)
      final url = 'https://api.open-meteo.com/v1/forecast?latitude=$lat&longitude=$lng&current=temperature_2m,relative_humidity_2m,weather_code,wind_speed_10m';
      final response = await Dio().get(url);
      final data = response.data['current'];

      return {
        'temp': data['temperature_2m'].round(),
        'condition': getWeatherCondition(data['weather_code']),
        'location': locationName,
        'humidity': data['relative_humidity_2m'],
        'windSpeed': data['wind_speed_10m'],
        'icon': getWeatherIcon(data['weather_code']),
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

  IconData getWeatherIcon(int? code) {
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

  String getWeatherCondition(int? code) {
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

  Future<Map<String, dynamic>?> scanImage(XFile image, {bool isSoil = false, String modelType = 'auto'}) async {
    final position = await _getCurrentLocation();
    final lat = position?.latitude;
    final lng = position?.longitude;

    try {
      final apiClient = ApiClient();
      final result = await apiClient.postFile('/scans', image.path, {
        'label': isSoil ? 'Soil_Sample' : 'Crop_Unknown',
        'isSoilAnalysis': isSoil.toString(),
        'latitude': lat?.toString() ?? '',
        'longitude': lng?.toString() ?? '',
        'modelType': modelType,  // Send selected AI model to backend
      });

      final scanData = result.data as Map<String, dynamic>;
      final enriched = <String, dynamic>{
        ...scanData,
        'imageUrl': scanData['imageUrl'] ?? '',
        'createdAt': scanData['createdAt'] ?? DateTime.now().toIso8601String(),
        'isSoilAnalysis': isSoil,
        'aiSource': 'backend',
      };

      await LocalDatabase.saveScan(enriched);
      if (FirebaseAuth.instance.currentUser != null) {
        await FirebaseFirestore.instance.collection('scans').add({
          ...enriched,
          "userId": FirebaseAuth.instance.currentUser!.uid,
          "timestamp": FieldValue.serverTimestamp(),
        });
      }
      return enriched;
    } catch (e) {
      debugPrint('Scan API error: $e');
      
      // Check if it's a connection error and fallback to on-device AI
      final errorMsg = e.toString().toLowerCase();
      if (errorMsg.contains('connection') || errorMsg.contains('timeout') || 
          errorMsg.contains('unavailable') || errorMsg.contains('failed to connect')) {
        debugPrint('Backend unreachable, falling back to on-device AI');
        try {
          final onDeviceResult = await _analyzeImageOnDevice(image.path, isSoil);
          await LocalDatabase.saveScan(onDeviceResult);
          // on-device does not use modelType
          return onDeviceResult;
        } catch (deviceError) {
          debugPrint('On-device analysis also failed: $deviceError');
          throw Exception('Backend unreachable and on-device analysis failed');
        }
      }
      
      rethrow;
    }
  }

  Future<Map<String, dynamic>> _analyzeImageOnDevice(String imagePath, bool isSoil) async {
    final analysis = await _onDeviceAI.analyzeImage(imagePath, isSoil: isSoil);
    
    if (analysis == null) {
      throw Exception('On-device AI model not loaded or analysis failed');
    }
    
    return {
      ...analysis,
      'imageUrl': 'local://scan_${DateTime.now().millisecondsSinceEpoch}',
      'createdAt': DateTime.now().toIso8601String(),
      'isSoilAnalysis': isSoil,
      'aiSource': 'on_device',
      'userId': FirebaseAuth.instance.currentUser?.uid ?? 'local_user',
      'cause': null,
      'cropHealth': null,
      'prevention': analysis['prevention'] ?? null,
      'chemicalClass': null,
      'suitableCrops': analysis['suitableCrops'] ?? null,
      'matchedDiseaseKey': null,
      'regionHint': null,
      'productResearch': null,
      'productResearchSource': null,
      'productResearchError': null,
      'weather': null,
      'confidence': analysis['confidence'] ?? 0.5,
    };
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

  Map<String, String> getRegionInfo(double? lat, double? lng) {
    if (lat == null || lng == null) return {'state': 'Unknown', 'climate': 'General'};
    if (lat > 28) return {'state': 'North India', 'climate': 'Cool/Dry'};
    if (lat < 15) return {'state': 'South India', 'climate': 'Hot/Humid'};
    if (lng < 75) return {'state': 'West India', 'climate': 'Arid/Dry'};
    if (lng > 85) return {'state': 'East India', 'climate': 'Tropical/Wet'};
    return {'state': 'Central India', 'climate': 'Moderate'};
  }
}

