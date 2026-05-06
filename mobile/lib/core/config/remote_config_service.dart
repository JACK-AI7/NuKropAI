import 'package:firebase_remote_config/firebase_remote_config.dart';
import 'package:flutter/foundation.dart';

class RemoteConfigService {
  static final FirebaseRemoteConfig _remoteConfig = FirebaseRemoteConfig.instance;

  static Future<void> initialize() async {
    try {
      await _remoteConfig.setConfigSettings(
        RemoteConfigSettings(
          fetchTimeout: const Duration(seconds: 15),
          minimumFetchInterval: const Duration(hours: 1),
        ),
      );

      await _remoteConfig.setDefaults({
        'nukrop_api_key': '',
        'base_url': 'http://10.0.2.2:3000/api',
        'ws_url': 'ws://10.0.2.2:3000',
        'ai_server_url': 'https://jaswanthbreddy-nukropai-farming-ai.hf.space/api/v1',
        'gemini_api_key': '',
      });

      await _remoteConfig.fetchAndActivate();
    } catch (e) {
      // Continue with defaults if fetch fails
      debugPrint('Remote Config fetch failed, using defaults: $e');
    }
  }

  static String get apiKey =>
      _remoteConfig.getString('nukrop_api_key');

  static String get baseUrl =>
      _remoteConfig.getString('base_url');

  static String get wsUrl =>
      _remoteConfig.getString('ws_url');

  static String get aiServerUrl =>
      _remoteConfig.getString('ai_server_url');

  static String get geminiApiKey =>
      _remoteConfig.getString('gemini_api_key');
}
