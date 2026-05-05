import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Provider for current server base URL (dynamic, from settings)
final serverUrlProvider = StateProvider<String>((ref) => 'http://10.0.2.2:3000/api');

/// Provider to load and save server URL
final serverConfigProvider = Provider((ref) => ServerConfigService());

/// Provider that gives the base URL without '/api' suffix
final serverBaseUrlProvider = Provider<String>((ref) {
  final fullUrl = ref.watch(serverUrlProvider);
  if (fullUrl.endsWith('/api')) {
    return fullUrl.substring(0, fullUrl.length - 4);
  }
  return fullUrl;
});

class ServerConfigService {
  static const String _key = 'server_url';
  static const String _defaultUrl = 'http://10.0.2.2:3000/api';

  Future<String> getServerUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_key) ?? _defaultUrl;
  }

  Future<void> saveServerUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_key, url);
  }

  String getBaseUrlWithoutApi(String fullUrl) {
    if (fullUrl.endsWith('/api')) {
      return fullUrl.substring(0, fullUrl.length - 4);
    }
    return fullUrl;
  }
}
