import 'package:flutter/material.dart';
import 'package:dio/dio.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/config/constants.dart';

class AIHealthScreen extends StatefulWidget {
  const AIHealthScreen({super.key});

  @override
  State<AIHealthScreen> createState() => _AIHealthScreenState();
}

class _AIHealthScreenState extends State<AIHealthScreen> {
  Map<String, dynamic>? _stats;
  Map<String, dynamic>? _health;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchStats();
  }

  Future<void> _fetchStats() async {
    setState(() => _isLoading = true);
    try {
      final dio = Dio();
      final statsResponse = await dio.get(
        '${AppConstants.aiServerUrl}/admin/stats',
        options: Options(headers: {'X-API-Key': 'nukrop_secret_dev'}),
      );
      final healthResponse = await dio.get('${AppConstants.aiServerUrl}/health');
      
      setState(() {
        _stats = statsResponse.data;
        _health = healthResponse.data;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('AI ENGINE HEALTH'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : RefreshIndicator(
              onRefresh: _fetchStats,
              child: SingleChildScrollView(
                padding: const EdgeInsets.all(20),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildStatusCard(),
                    const SizedBox(height: 24),
                    const Text('LOADED MODELS', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                    const SizedBox(height: 12),
                    _buildModelsList(),
                    const SizedBox(height: 24),
                    const Text('PERFORMANCE METRICS', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.2)),
                    const SizedBox(height: 12),
                    _buildMetricsGrid(),
                  ],
                ),
              ),
            ),
    );
  }

  Widget _buildStatusCard() {
    final isOnline = _health?['status'] == 'ok';
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.05),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: isOnline ? Colors.green.withOpacity(0.3) : Colors.red.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Icon(isOnline ? Icons.check_circle : Icons.error, color: isOnline ? Colors.green : Colors.red, size: 40),
          const SizedBox(width: 16),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(isOnline ? 'SYSTEM OPERATIONAL' : 'SYSTEM OFFLINE', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              Text('Hugging Face Space: ${AppConstants.aiServerUrl}', style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 12)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildModelsList() {
    final models = _health?['models'] as Map<String, dynamic>? ?? {};
    return Wrap(
      spacing: 8,
      runSpacing: 8,
      children: models.entries.map((e) {
        return Chip(
          label: Text(e.key.toUpperCase()),
          backgroundColor: e.value ? Colors.green.withOpacity(0.2) : Colors.red.withOpacity(0.2),
          labelStyle: TextStyle(color: e.value ? Colors.green : Colors.red, fontSize: 10, fontWeight: FontWeight.bold),
        );
      }).toList(),
    );
  }

  Widget _buildMetricsGrid() {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 12,
      crossAxisSpacing: 12,
      childAspectRatio: 1.5,
      children: [
        _buildMetricItem('TOTAL REQS', _stats?['total_requests']?.toString() ?? '0', Icons.analytics),
        _buildMetricItem('UPTIME', '${(_stats?['uptime_seconds'] ?? 0) ~/ 60}m', Icons.timer),
        _buildMetricItem('REDIS CACHE', _health?['redis'] == true ? 'ACTIVE' : 'OFF', Icons.storage),
        _buildMetricItem('ERRORS', _stats?['error_count']?.toString() ?? '0', Icons.bug_report),
      ],
    );
  }

  Widget _buildMetricItem(String title, String value, IconData icon) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.03),
        borderRadius: BorderRadius.circular(16),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, color: AppColors.accent, size: 20),
          const SizedBox(height: 4),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
          Text(title, style: TextStyle(color: Colors.white.withOpacity(0.4), fontSize: 10)),
        ],
      ),
    );
  }
}
