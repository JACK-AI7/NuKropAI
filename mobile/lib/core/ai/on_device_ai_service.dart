import 'package:tflite_flutter/tflite_flutter.dart';
import 'package:image/image.dart' as img;
import 'dart:io';
import 'package:flutter/services.dart' show rootBundle;

class OnDeviceAIService {
  Interpreter? _interpreter;
  List<String>? _labels;
  static const String _modelPath = 'assets/models/crop_disease_model.tflite';
  static const String _labelsPath = 'assets/models/crop_disease_labels.txt';

  // Singleton
  static final OnDeviceAIService _instance = OnDeviceAIService._internal();
  factory OnDeviceAIService() => _instance;
  OnDeviceAIService._internal();

  /// Load the TFLite model and labels from assets
  Future<bool> loadModel() async {
    try {
      // Load model from assets
      final modelData = await rootBundle.load(_modelPath);
      _interpreter = Interpreter.fromBuffer(modelData.buffer.asUint8List());

      // Load labels
      final labelsData = await rootBundle.loadString(_labelsPath);
      _labels = labelsData.split('\n').where((l) => l.trim().isNotEmpty).toList();

      return true;
    } catch (e) {
      return false;
    }
  }

  /// Run inference on an image file
  Future<Map<String, dynamic>?> analyzeImage(String imagePath, {bool isSoil = false}) async {
    if (_interpreter == null || _labels == null) return null;

    try {
      final imageBytes = await File(imagePath).readAsBytes();
      final image = img.decodeImage(imageBytes);
      if (image == null) return null;

      final resized = img.copyResize(image, width: 224, height: 224);

      final input = List.filled(1 * 224 * 224 * 3, 0.0).reshape([1, 224, 224, 3]);
      for (int y = 0; y < 224; y++) {
        for (int x = 0; x < 224; x++) {
          final pixel = resized.getPixel(x, y);
          input[0][y][x][0] = pixel.r / 255.0;
          input[0][y][x][1] = pixel.g / 255.0;
          input[0][y][x][2] = pixel.b / 255.0;
        }
      }

      final output = List.filled(1 * _labels!.length, 0.0).reshape([1, _labels!.length]);
      _interpreter!.run(input, output);

      final probabilities = output[0];
      int maxIndex = 0;
      double maxProb = probabilities[0];
      for (int i = 1; i < probabilities.length; i++) {
        if (probabilities[i] > maxProb) {
          maxProb = probabilities[i];
          maxIndex = i;
        }
      }

      final predictedLabel = _labels![maxIndex];
      return _parseLabelToAnalysis(predictedLabel, maxProb, isSoil);
    } catch (e) {
      return null;
    }
  }

  Map<String, dynamic> _parseLabelToAnalysis(String label, double confidence, bool isSoil) {
    final parts = label.split('_');

    if (isSoil) {
      return {
        'soilType': parts[0],
        'soilHealth': 'Moderately fertile',
        'nutrients': 'Apply balanced NPK fertilizer',
        'npk': [20, 20, 20],
      };
    }

    return {
      'plantName': parts[0],
      'diseaseName': parts.length > 1 ? parts.sublist(1).join(' ') : 'Healthy',
      'confidence': confidence,
      'severity': confidence > 0.8 ? 'High' : (confidence > 0.6 ? 'Medium' : 'Low'),
      'treatment': 'Consult local agricultural expert',
      'fertilizer': 'Apply NPK as per soil test',
      'pesticide': 'Use recommended pesticides',
      'npk': [15, 15, 15],
    };
  }

  bool get isModelLoaded => _interpreter != null && _labels != null;
}
