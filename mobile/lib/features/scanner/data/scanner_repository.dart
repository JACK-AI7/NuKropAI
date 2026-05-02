import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';

final scannerRepositoryProvider = Provider((ref) => ScannerRepository(ref.read(apiClientProvider)));

class ScannerRepository {
  final ApiClient _apiClient;
  ScannerRepository(this._apiClient);

  Future<List<Map<String, dynamic>>> getHistory() async {
    final response = await _apiClient.get('/scans/history');
    if (response.data is List) {
      return List<Map<String, dynamic>>.from(response.data);
    }
    throw Exception('Invalid scan history response from server');
  }
}

final scanHistoryProvider = FutureProvider<List<Map<String, dynamic>>>((ref) {
  return ref.read(scannerRepositoryProvider).getHistory();
});
