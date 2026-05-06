import 'dart:io';
import 'package:dio/dio.dart';
import '../config/remote_config_service.dart';

class CloudAIService {
  final Dio _dio = Dio();
  final String _baseUrl = RemoteConfigService.aiServerUrl;

  /// Detect pests using YOLO11 on the cloud server
  Future<List<Map<String, dynamic>>> detectPests(String imagePath) async {
    try {
      FormData formData = FormData.fromMap({
        "file": await MultipartFile.fromFile(imagePath),
      });

      final response = await _dio.post("$_baseUrl/detect/pest", data: formData);
      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(response.data['detections']);
      }
    } catch (e) {
      print("Cloud Pest Detection Error: $e");
    }
    return [];
  }

  /// Detect maize diseases using the specialized maize model
  Future<List<Map<String, dynamic>>> detectMaizeDisease(String imagePath) async {
    try {
      FormData formData = FormData.fromMap({
        "file": await MultipartFile.fromFile(imagePath),
      });

      final response = await _dio.post("$_baseUrl/detect/maize", data: formData);
      if (response.statusCode == 200) {
        return List<Map<String, dynamic>>.from(response.data['results']);
      }
    } catch (e) {
      print("Cloud Maize Detection Error: $e");
    }
    return [];
  }

  /// Get crop recommendation based on NPK and environmental data
  Future<Map<String, dynamic>> getCropRecommendation({
    required double n,
    required double p,
    required double k,
    required double temp,
    required double humidity,
    required double ph,
    required double rainfall,
  }) async {
    try {
      final response = await _dio.post(
        "$_baseUrl/recommend/crop",
        queryParameters: {
          "n": n,
          "p": p,
          "k": k,
          "temp": temp,
          "humidity": humidity,
          "ph": ph,
          "rainfall": rainfall,
        },
      );
      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(response.data);
      }
    } catch (e) {
      print("Cloud Crop Recommendation Error: $e");
    }
    return {};
  }

  /// Chat with the AI Agronomist (LLM)
  Future<String> chatWithAgronomist(String prompt) async {
    try {
      final response = await _dio.post(
        "$_baseUrl/chat/agronomist",
        queryParameters: {"prompt": prompt},
      );
      if (response.statusCode == 200) {
        return response.data['response'] ?? "I'm sorry, I couldn't process that.";
      }
    } catch (e) {
      print("Cloud Agronomist Error: $e");
    }
    return "The AI Agronomist is currently offline.";
  }
  /// Advanced agricultural analysis using MLLMs (Agri-LLaVA)
  Future<Map<String, dynamic>> analyzeAdvanced(String imagePath, {String? prompt}) async {
    try {
      FormData formData = FormData.fromMap({
        "file": await MultipartFile.fromFile(imagePath),
        "prompt": prompt ?? "Analyze this crop health and suggest treatment.",
      });

      final response = await _dio.post("$_baseUrl/analyze/agri-llava", data: formData);
      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(response.data);
      }
    } catch (e) {
      print("Advanced Analysis Error: $e");
    }
    return {};
  }

  /// General crop disease analysis using the new multi-model router
  Future<Map<String, dynamic>> analyzeCrop(String imagePath) async {
    try {
      FormData formData = FormData.fromMap({
        "file": await MultipartFile.fromFile(imagePath),
      });

      final response = await _dio.post("$_baseUrl/analyze/crop", data: formData);
      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(response.data);
      }
    } catch (e) {
      print("Cloud Crop Analysis Error: $e");
    }
    return {};
  }

  /// Classify soil type using the cloud TF model
  Future<Map<String, dynamic>> classifySoil(String imagePath) async {
    try {
      FormData formData = FormData.fromMap({
        "file": await MultipartFile.fromFile(imagePath),
      });

      final response = await _dio.post("$_baseUrl/classify/soil", data: formData);
      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(response.data);
      }
    } catch (e) {
      print("Cloud Soil Classification Error: $e");
    }
    return {};
  }

  /// Get NPK recommendation using the cloud Sklearn model
  Future<Map<String, dynamic>> recommendNPK(double n, double p, double k) async {
    try {
      final response = await _dio.post(
        "$_baseUrl/recommend/npk",
        queryParameters: {"n": n, "p": p, "k": k},
      );
      if (response.statusCode == 200) {
        return Map<String, dynamic>.from(response.data);
      }
    } catch (e) {
      print("Cloud NPK Recommendation Error: $e");
    }
    return {};
  }
}
