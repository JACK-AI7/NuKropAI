import 'package:firebase_remote_config/firebase_remote_config.dart';

class RemoteConfigService {
  static final FirebaseRemoteConfig _remoteConfig = FirebaseRemoteConfig.instance;

  static Future<void> initialize() async {
    await _remoteConfig.setConfigSettings(
      RemoteConfigSettings(
        fetchTimeout: const Duration(seconds: 15),
        minimumFetchInterval: const Duration(hours: 1),
      ),
    );

    await _remoteConfig.fetchAndActivate();
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
