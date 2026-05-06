import 'package:firebase_remote_config/firebase_remote_config.dart';

class RemoteConfigService {
  static final RemoteConfigService _instance = RemoteConfigService._internal();
  factory RemoteConfigService() => _instance;
  RemoteConfigService._internal();

  late FirebaseRemoteConfig _remoteConfig;

  Future<void> initialize() async {
    _remoteConfig = FirebaseRemoteConfig.instance;
    await _remoteConfig.setConfigSettings(RemoteConfigSettings(
      fetchTimeout: const Duration(seconds: 10),
      minimumFetchInterval: const Duration(hours: 1),
    ));
    await _remoteConfig.setDefaults({
      'gemini_api_key': '',
      'ai_server_url': 'https://your-server.com',
    });
    await _remoteConfig.fetchAndActivate();
  }

  static String get geminiApiKey => RemoteConfigService()._remoteConfig.getString('gemini_api_key');
  static String get aiServerUrl => RemoteConfigService()._remoteConfig.getString('ai_server_url');
}