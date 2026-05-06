import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../constants/app_constants.dart';

final apiClientProvider = Provider((ref) => ApiClient());

class ApiClient {
  final Dio _dio = Dio(BaseOptions(
    baseUrl: AppConstants.baseUrl,
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 60),
    sendTimeout: const Duration(seconds: 60),
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
      onError: (error, handler) async {
        if (error.type == DioExceptionType.connectionTimeout ||
            error.type == DioExceptionType.receiveTimeout ||
            error.type == DioExceptionType.sendTimeout ||
            error.type == DioExceptionType.connectionError) {
          error = DioException(
            requestOptions: error.requestOptions,
            error: 'Unable to connect to server. Please check your internet connection and server address.',
            type: error.type,
          );
        }
        return handler.next(error);
      },
    ));
  }

  Future<Response> get(String path, {Map<String, dynamic>? queryParameters, int retries = 2}) async {
    try {
      return await _dio.get(path, queryParameters: queryParameters);
    } catch (e) {
      if (retries > 0 && e is DioException) {
        await Future.delayed(Duration(seconds: 1));
        return await _dio.get(path, queryParameters: queryParameters);
      }
      rethrow;
    }
  }

  Future<Response> post(String path, {dynamic data, int retries = 2}) async {
    try {
      return await _dio.post(path, data: data);
    } catch (e) {
      if (retries > 0 && e is DioException) {
        await Future.delayed(Duration(seconds: 1));
        return await _dio.post(path, data: data);
      }
      rethrow;
    }
  }

  Future<Response> postFile(String path, String filePath, Map<String, dynamic> data, {int retries = 2}) async {
    try {
      final formData = FormData.fromMap({
        ...data,
        'image': await MultipartFile.fromFile(filePath),
      });
      return await _dio.post(path, data: formData);
    } catch (e) {
      if (retries > 0 && e is DioException) {
        await Future.delayed(Duration(seconds: 1));
        final formData = FormData.fromMap({
          ...data,
          'image': await MultipartFile.fromFile(filePath),
        });
        return await _dio.post(path, data: formData);
      }
      rethrow;
    }
  }

  /// Check if backend is reachable
  Future<bool> checkHealth() async {
    try {
      final response = await _dio.get('/health', options: Options(validateStatus: (status) => status == 200));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }

  /// Update base URL at runtime
  void updateBaseUrl(String url) {
    _dio.options.baseUrl = url;
  }
}
