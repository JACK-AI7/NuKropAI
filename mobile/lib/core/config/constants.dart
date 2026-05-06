import 'remote_config_service.dart';

class AppConstants {
  // Backend API URL - dynamically loaded from Firebase Remote Config
  static String get baseUrl => RemoteConfigService.baseUrl;
  
  // Hugging Face AI Server URL - dynamically loaded from Firebase Remote Config
  static String get aiServerUrl => RemoteConfigService.aiServerUrl;
}

