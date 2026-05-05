import 'package:google_generative_ai/google_generative_ai.dart';
import 'package:flutter/foundation.dart';
import 'dart:io';
import 'dart:async';
import 'package:shared_preferences/shared_preferences.dart';

class LLMService {
  static const String _defaultApiKey = ""; // Set via Settings or --dart-define
  late GenerativeModel _model;
  bool _isInitialized = false;
  String? _apiKey;
  String _currentModel = 'gemini-1.5-flash';
  
  // Agricultural specialist LLM configurations
  static const String cropSeek = 'CropSeek-LLM (Fine-tuned DeepSeek-R1)';
  static const String agriChat = 'AgriChat MLLM (Interactive Diagnostics)';
  static const String agriGPT = 'AgriGPT-VL (Vision-Language Reasoning)';
  static const String agriM = 'AgriM-LLM (Enhanced Vision Encoder)';
  static const String agriLLaVA = 'Agri-LLaVA (Conversational Diagnostics)';
  static const String phi4 = 'Phi-4 Multimodal (Low-latency Edge)';
  static const String llamaVision = 'Llama 3.2 Vision (Open Weights)';
  static const String qwenVL = 'Qwen 2.5 VL (Apache 2.0)';
  
  // Available Gemini models for different use cases
  // Using stable v1 API models (not -latest aliases which can be deprecated)
  static const Map<String, String> geminiModels = {
    'Gemini 1.5 Flash': 'gemini-1.5-flash',
    'Gemini 1.5 Pro': 'gemini-1.5-pro',
    'Gemini 1.0 Pro': 'gemini-pro',
  };

  LLMService() {
    _loadKeyAndInit();
  }

    Future<void> _loadKeyAndInit() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      String? storedKey = prefs.getString('gemini_api_key');
      if (storedKey == null || storedKey.trim().isEmpty) {
        storedKey = _defaultApiKey;
      }
      _apiKey = storedKey;
      
      // Load selected model
      String selectedModel = prefs.getString('gemini_model') ?? 'gemini-1.5-flash';
      _currentModel = selectedModel;
      
      if (_apiKey == null || _apiKey!.isEmpty) {
        debugPrint('LLM: No API key available. Using default (empty) key.');
        _apiKey = _defaultApiKey;
      }
      
      // Use v1 API for stability (v1beta may have regional restrictions)
      _model = GenerativeModel(
        model: _currentModel,
        apiKey: _apiKey!,
        systemInstruction: _getSystemInstruction(),
      );
      _isInitialized = true;
      debugPrint('LLM initialized with $_currentModel (v1 API)');
    } catch (e) {
      debugPrint('LLM Init Error: $e');
      _isInitialized = false;
    }
  }

  Content _getSystemInstruction() {
    return Content.system('''
You are NuKropAI, an expert agricultural assistant for Indian farmers.
You specialize in crop disease identification, pest management, soil health, and sustainable farming.

Agricultural AI Models Available:
- AgriChat MLLM: Interactive diagnostic reasoning for species ID, disease classification, fruit counting
- AgriGPT-VL: Vision-language model trained on Agri-3M-VL corpus (3,000+ classes, 682 diseases)
- AgriM-LLM: Enhanced vision encoder with 84% pest ID accuracy
- Agri-LLaVA: Open-source LLaVA with agricultural domain expertise
- CropSeek-LLM: Fine-tuned for crop-specific analysis

General Multimodal Models (adaptable for agriculture):
- Llama 3.2 Vision: Open-weights, local/cloud capable
- Qwen 2.5 VL: Apache 2.0, vision transformer + language model
- Phi-4 Multimodal: MIT license, low-latency edge optimized

Datasets & Benchmarks:
- AgriMM: 121k images, 607k expert-aligned QA pairs
- LLMI-CDP: Q-Former for precise pest capture
- AgroBench: 203 crop types, 682 disease categories

ALWAYS respond with valid JSON when asked for structured data. No markdown blocks.
When recommending products:
- Mention active ingredient (e.g., Imidacloprid 17.8% SL)
- Give dosage per litre or per kg
- Suggest where to buy (Amazon India, AgriBegri)
- Include safety notes (PPE, PHI)

Be concise but thorough. Use metric units and Indian agricultural context.
''');
  }

  Future<void> init() async {
    if (!_isInitialized) {
      await _loadKeyAndInit();
    }
  }

  Future<void> updateModel(String modelName) async {
    if (geminiModels.values.contains(modelName)) {
      _currentModel = modelName;
      // Use v1 API for stability
      _model = GenerativeModel(
        model: _currentModel,
        apiKey: _apiKey!,
        systemInstruction: _getSystemInstruction(),
      );
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('gemini_model', modelName);
      _isInitialized = true;
      debugPrint('LLM model updated to $_currentModel (v1 API)');
    }
  }

  Future<void> updateApiKey(String newKey) async {
    _apiKey = newKey;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('gemini_api_key', newKey);
    
    // Use v1 API for stability
    _model = GenerativeModel(
      model: _currentModel,
      apiKey: _apiKey!,
      systemInstruction: _getSystemInstruction(),
    );
    _isInitialized = true;
    debugPrint('LLM API key updated (v1 API)');
  }

  /// Generate text response, optionally with image(s) for multimodal analysis
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

        // Add image if provided (multimodal analysis)
        if (imagePaths != null && imagePaths.isNotEmpty) {
          final List<Part> parts = [];
          for (final path in imagePaths) {
            final file = File(path);
            if (await file.exists()) {
              final bytes = await file.readAsBytes();
              parts.add(DataPart('image/jpeg', bytes));
            }
          }
          if (parts.isNotEmpty) {
            content.add(Content.multi([TextPart(prompt), ...parts]));
          } else {
            content.add(Content.text(prompt));
          }
        } else {
          content.add(Content.text(prompt));
        }

        final response = await _model.generateContent(content).timeout(const Duration(seconds: 30));
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
          return "Error: ${e.toString()}. Please check your internet connection and API key.";
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
  
  String get currentModel => _currentModel;
}
