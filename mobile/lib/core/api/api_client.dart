import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../config/constants.dart';

final apiClientProvider = Provider((ref) => ApiClient());

class ApiClient {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: AppConstants.baseUrl,
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
  ));

  ApiClient() {
    _init();
  }

  Future<void> _init() async {
    final prefs = await SharedPreferences.getInstance();
    final customUrl = prefs.getString('server_url');
    if (customUrl != null && customUrl.isNotEmpty) {
      _dio.options.baseUrl = customUrl;
    }

    _dio.interceptors.add(InterceptorsWrapper(
      onRequest: (options, handler) async {
        final p = await SharedPreferences.getInstance();
        final token = p.getString('token');
        if (token != null) {
          options.headers['Authorization'] = 'Bearer $token';
        }
        return handler.next(options);
      },
    ));
  }

  Future<Response> get(String path, {Map<String, dynamic>? queryParameters}) async {
    try {
      return await _dio.get(path, queryParameters: queryParameters);
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> post(String path, {dynamic data}) async {
    try {
      return await _dio.post(path, data: data);
    } catch (e) {
      rethrow;
    }
  }

  Future<Response> postFile(String path, String filePath, Map<String, dynamic> data) async {
    try {
      final formData = FormData.fromMap({
        ...data,
        'image': await MultipartFile.fromFile(filePath),
      });
      return await _dio.post(path, data: formData);
    } catch (e) {
      rethrow;
    }
  }
}
