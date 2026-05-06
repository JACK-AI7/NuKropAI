import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/api/scanner_service.dart';

class ForecastScreen extends ConsumerStatefulWidget {
  const ForecastScreen({super.key});

  @override
  ConsumerState<ForecastScreen> createState() => _ForecastScreenState();
}

class _ForecastScreenState extends ConsumerState<ForecastScreen> {
  Map<String, dynamic>? _forecast;
  Map<String, dynamic>? _satellite;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _loadData();
  }

  Future<void> _loadData() async {
    try {
      final service = ref.read(scannerServiceProvider);
      final forecast = await service.getForecast();
      final satellite = await service.getSatelliteAnalysis();
      setState(() {
        _forecast = forecast;
        _satellite = satellite;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      print('Forecast error: $e');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('AI PREDICTIVE FORECAST'),
        backgroundColor: Colors.transparent,
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : SingleChildScrollView(
              padding: const EdgeInsets.all(20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildSatelliteCard(),
                  const SizedBox(height: 24),
                  const Text('7-DAY PEST RISK FORECAST', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.5)),
                  const SizedBox(height: 16),
                  _buildRiskChart(),
                  const SizedBox(height: 32),
                  const Text('IRRIGATION INTELLIGENCE', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.5)),
                  const SizedBox(height: 12),
                  _buildIrrigationCard(),
                ],
              ),
            ),
    );
  }

  Widget _buildSatelliteCard() {
    final ndvi = _satellite?['ndvi'] ?? 0.0;
    final color = ndvi > 0.6 ? Colors.green : (ndvi > 0.4 ? Colors.orange : Colors.red);
    
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 28, highlight: true),
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('SATELLITE NDVI', style: TextStyle(color: Colors.white54, fontWeight: FontWeight.bold, fontSize: 10)),
                  Text('FIELD HEALTH', style: TextStyle(fontWeight: FontWeight.w900, fontSize: 18)),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(color: color.withOpacity(0.2), borderRadius: BorderRadius.circular(10)),
                child: Text('${(ndvi * 100).toInt()}%', style: TextStyle(color: color, fontWeight: FontWeight.bold)),
              ),
            ],
          ),
          const SizedBox(height: 20),
          LinearProgressIndicator(value: ndvi, backgroundColor: Colors.white10, color: color, minHeight: 8),
          const SizedBox(height: 12),
          Text(_satellite?['prediction'] ?? 'Analyzing...', style: const TextStyle(fontStyle: FontStyle.italic, color: Colors.white70)),
        ],
      ),
    );
  }

  Widget _buildRiskChart() {
    if (_forecast == null) return const SizedBox();
    
    final points = _forecast!.entries.toList();
    return Container(
      height: 200,
      padding: const EdgeInsets.all(16),
      decoration: AppColors.glassDecoration(radius: 24),
      child: LineChart(
        LineChartData(
          gridData: const FlGridData(show: false),
          titlesData: const FlTitlesData(show: false),
          borderData: FlBorderData(show: false),
          lineBarsData: [
            LineChartBarData(
              spots: points.asMap().entries.map((e) => FlSpot(e.key.toDouble(), e.value.value['pest_risk'])).toList(),
              isCurved: true,
              color: AppColors.accent,
              barWidth: 4,
              isStrokeCapRound: true,
              dotData: const FlDotData(show: false),
              belowBarData: BarAreaData(show: true, color: AppColors.accent.withOpacity(0.1)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildIrrigationCard() {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: AppColors.glassDecoration(radius: 24),
      child: Row(
        children: [
          const Icon(Icons.water_drop, color: Colors.blueAccent, size: 40),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('MOISTURE STRESS: LOW', style: TextStyle(fontWeight: FontWeight.bold)),
                Text('Next irrigation recommended in 3 days based on satellite data.', style: TextStyle(color: Colors.white.withOpacity(0.5), fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
