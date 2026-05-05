import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';

/// Provider for connectivity service
final connectivityServiceProvider = Provider((ref) => ConnectivityService(ref.watch(apiClientProvider)));

/// Provider exposing current connectivity status as list of results
final connectivityStatusProvider = StreamProvider<List<ConnectivityResult>>((ref) {
  final service = ref.watch(connectivityServiceProvider);
  return service.connectivityStream;
});

/// Provider indicating if backend is reachable
final backendHealthProvider = StreamProvider<bool>((ref) {
  final service = ref.watch(connectivityServiceProvider);
  return service.backendHealthStream;
});

class ConnectivityService {
  final ApiClient _apiClient;
  final Connectivity _connectivity = Connectivity();
  StreamController<List<ConnectivityResult>>? _connectivityController;
  StreamController<bool>? _healthController;
  Timer? _healthCheckTimer;

  ConnectivityService(this._apiClient) {
    _connectivityController = StreamController<List<ConnectivityResult>>.broadcast();
    _healthController = StreamController<bool>.broadcast();
    _startMonitoring();
  }

  Stream<List<ConnectivityResult>> get connectivityStream => _connectivityController!.stream;
  Stream<bool> get backendHealthStream => _healthController!.stream;

  void _startMonitoring() {
    // Initial check
    _checkConnectivity();
    _checkBackendHealth();

    // Listen to connectivity changes
    _connectivity.onConnectivityChanged.listen((results) {
      _connectivityController!.add(results);
      if (results != ConnectivityResult.none) {
        // When network is available, check backend health after a short delay
        Future.delayed(const Duration(seconds: 2), _checkBackendHealth);
      } else {
        _healthController!.add(false);
      }
    });

    // Periodic backend health check (every 30 seconds)
    _healthCheckTimer = Timer.periodic(const Duration(seconds: 30), (timer) {
      _checkBackendHealth();
    });
  }

  Future<void> _checkConnectivity() async {
    try {
      final results = await _connectivity.checkConnectivity();
      _connectivityController!.add(results);
    } catch (e) {
      _connectivityController!.add([ConnectivityResult.none]);
    }
  }

  Future<void> _checkBackendHealth() async {
    try {
      final isHealthy = await _apiClient.checkHealth();
      _healthController!.add(isHealthy);
    } catch (e) {
      _healthController!.add(false);
    }
  }

  /// Get current connectivity status
  Future<List<ConnectivityResult>> getCurrentConnectivity() async {
    return await _connectivity.checkConnectivity();
  }

  /// Check if backend is currently reachable
  Future<bool> isBackendReachable() async {
    return await _apiClient.checkHealth();
  }

  void dispose() {
    _connectivityController?.close();
    _healthController?.close();
    _healthCheckTimer?.cancel();
  }
}
