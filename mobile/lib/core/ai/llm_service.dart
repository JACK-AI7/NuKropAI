import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:flutter/foundation.dart';
import 'dart:io';
import 'dart:async';
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class LLMService {
  static const String _defaultApiKey = ""; // Removed for security. Add your key in Settings or via --dart-define
  late GenerativeModel _model;
  bool _isInitialized = false;
  String? _apiKey;
  static const Duration _timeout = Duration(seconds: 30);

  // Agricultural specialist LLM configurations
  static const String cropSeek = 'CropSeek-LLM (Fine-tuned DeepSeek-R1)';
  static const String agriChat = 'AgriChat MLLM (Interactive Diagnostics)';
  static const String agriGPT = 'AgriGPT-VL (Vision-Language Reasoning)';
  static const String agriLLaVA = 'Agri-LLaVA (Conversational Diagnostics)';
  static const String phi4 = 'Phi-4 Multimodal (Low-latency Edge)';
  static const String llamaVision = 'Llama 3.2 Vision (Open Weights)';
  static const String qwenVL = 'Qwen 2.5 VL (Apache 2.0)';

  LLMService() {
    _loadKeyAndInit();
  }

  Future<void> _loadKeyAndInit() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      String? storedKey = prefs.getString('gemini_api_key');
      if (storedKey == null || storedKey.trim().isEmpty) {
        storedKey = _defaultApiKey; // fall back to default
      }
      _apiKey = storedKey;
      if (_apiKey == null || _apiKey!.isEmpty) {
        debugPrint('LLM: No API key available. Using default key.');
        _apiKey = _defaultApiKey;
      }
      _model = GenerativeModel(
        model: 'gemini-1.5-flash-latest',
        apiKey: _apiKey!,
        systemInstruction: Content.system('''
You are NuKropAI, an expert agricultural assistant for Indian farmers.
You specialize in:
- Crop disease identification and treatment
- Pest management with specific pesticide recommendations (Indian market)
- Soil health and fertilizer advice (NPK)
- Sustainable farming practices
- Weather-aware guidance

ALWAYS respond with valid JSON when asked for structured data. No markdown blocks.
When recommending products:
- Mention active ingredient (e.g., Imidacloprid 17.8% SL)
- Give dosage per litre or per kg
- Suggest where to buy (Amazon India, AgriBegri)
- Include safety notes (PPE, PHI)

Be concise but thorough.
'''),
      );
      _isInitialized = true;
      debugPrint('LLM initialized with Gemini 1.5 Flash');
    } catch (e) {
      debugPrint('LLM Init Error: $e');
      _isInitialized = false;
    }
  }

  Future<void> init() async {
    if (!_isInitialized) {
      await _loadKeyAndInit();
    }
  }

  /// Generate text response, optionally with image(s)
  Future<String> generateResponse(String prompt, {List<String>? imagePaths, int maxRetries = 2}) async {
    if (!_isInitialized) {
      await _loadKeyAndInit();
    }
    if (!_isInitialized) {
      return "Error: LLM service not initialized. Check your internet connection or API key.";
    }

    int attempt = 0;
    while (attempt <= maxRetries) {
      try {
        final List<Content> content = [];

        content.add(Content.text(prompt));

        if (imagePaths != null && imagePaths.isNotEmpty) {
          for (final path in imagePaths) {
            final file = File(path);
            if (await file.exists()) {
              final bytes = await file.readAsBytes();
              content.add(Content.data('image/jpeg', bytes));
            }
          }
        }

        final response = await _model.generateContent(content).timeout(_timeout);
        return response.text ?? "I'm sorry, I couldn't generate a response.";
      } on TimeoutException {
        attempt++;
        if (attempt > maxRetries) {
          return "Error: Request timed out. Please check your internet connection and try again.";
        }
        await Future.delayed(Duration(milliseconds: 400 * attempt));
      } catch (e) {
        attempt++;
        if (attempt > maxRetries) {
          debugPrint('LLM Generation Error after $attempt retries: $e');
          return "Error: $e. Please check your internet connection and API key.";
        }
        await Future.delayed(Duration(milliseconds: 400 * attempt));
      }
    }
    return "Error: Failed to generate response after retries.";
  }

  /// Simple text-only generation (for chat, product research)
  Future<String> generateText(String prompt) async {
    return generateResponse(prompt);
  }

  /// Check if API key is configured
  bool get isConfigured => _apiKey != null && _apiKey!.isNotEmpty && _apiKey != _defaultApiKey;
}