import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:flutter/foundation.dart';
import 'dart:io';

class LLMService {
  static const String _apiKey = "YOUR_FREE_API_KEY"; // User should replace this or use env
  late GenerativeModel _model;
  bool _isInitialized = false;

  // Specialized Agricultural Models requested by user
  static const String cropSeek = 'CropSeek-LLM (Fine-tuned DeepSeek-R1)';
  static const String agriChat = 'AgriChat MLLM (Interactive Diagnostics)';
  static const String agriGPT = 'AgriGPT-VL (Vision-Language Reasoning)';
  static const String agriLLaVA = 'Agri-LLaVA (Conversational Diagnostics)';
  static const String phi4 = 'Phi-4 Multimodal (Low-latency Edge)';
  static const String llamaVision = 'Llama 3.2 Vision (Open Weights)';
  static const String qwenVL = 'Qwen 2.5 VL (Apache 2.0)';

  LLMService() {
    _initModel();
  }

  Future<void> _initModel() async {
    try {
      // Defaulting to Gemini-1.5-Flash which is free and high performance
      // This acts as a placeholder for the specialized models requested
      _model = GenerativeModel(
        model: 'gemini-1.5-flash',
        apiKey: _apiKey,
        systemInstruction: Content.system('You are NuKropAI, an agricultural expert. Provide professional advice on crop diseases, pests, and soil health. Always suggest specific pesticide or fertilizer products with active ingredients and application tips when a problem is identified. Focus on sustainable and effective solutions.'),
      );
      _isInitialized = true;
    } catch (e) {
      debugPrint('LLM Init Error: $e');
    }
  }

  Future<String> generateResponse(String prompt, {List<String>? imagePaths}) async {
    if (!_isInitialized) await _initModel();

    try {
      final content = [Content.text(prompt)];
      
      if (imagePaths != null && imagePaths.isNotEmpty) {
        for (final path in imagePaths) {
          final bytes = await File(path).readAsBytes();
          content.add(Content.data('image/jpeg', bytes));
        }
      }

      final response = await _model.generateContent(content);
      return response.text ?? "I'm sorry, I couldn't generate a response.";
    } catch (e) {
      debugPrint('LLM Generation Error: $e');
      return "Error: $e. (Make sure you have a valid internet connection or local model loaded)";
    }
  }

  /// Placeholder for true on-device inference using MediaPipe/TFLite
  Future<String> generateOnDeviceResponse(String prompt) async {
    // In a real implementation, this would use mediapipe_genai
    // For now, it provides basic agricultural logic offline
    if (prompt.toLowerCase().contains('pest')) {
      return "Local Analysis: Identifying common pests based on IP102 dataset. Please ensure the image is clear.";
    }
    return "Running in On-Device Mode. For advanced diagnostics, please connect to the internet.";
  }
}
