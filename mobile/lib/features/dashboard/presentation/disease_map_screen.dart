import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong2.dart';
import 'package:dio/dio.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/config/constants.dart';

class DiseaseMapScreen extends StatefulWidget {
  const DiseaseMapScreen({super.key});

  @override
  State<DiseaseMapScreen> createState() => _DiseaseMapScreenState();
}

class _DiseaseMapScreenState extends State<DiseaseMapScreen> {
  List<Marker> _markers = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchHeatmapData();
  }

  Future<void> _fetchHeatmapData() async {
    try {
      final dio = Dio();
      final response = await dio.get(
        '${AppConstants.aiServerUrl}/analytics/heatmap',
        options: Options(headers: {'X-API-Key': 'nukrop_secret_dev'}),
      );
      
      final List<dynamic> features = response.data['features'];
      setState(() {
        _markers = features.map((f) {
          final coords = f['geometry']['coordinates'];
          final props = f['properties'];
          return Marker(
            point: LatLng(coords[1], coords[0]),
            width: 40,
            height: 40,
            child: GestureDetector(
              onTap: () => _showOutbreakDetails(props),
              child: Icon(
                Icons.location_on,
                color: props['severity'] == 'High' ? Colors.red : Colors.orange,
                size: 40,
              ),
            ),
          );
        }).toList();
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      print('Heatmap error: $e');
    }
  }

  void _showOutbreakDetails(Map<String, dynamic> props) {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF1E293B),
      shape: const RoundedRectangleBorder(borderRadius: BorderRadius.vertical(top: Radius.circular(24))),
      builder: (ctx) => Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.warning_amber_rounded, color: Colors.redAccent),
                const SizedBox(width: 12),
                Text('OUTBREAK DETECTED', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.w900, letterSpacing: 1.5)),
              ],
            ),
            const SizedBox(height: 16),
            Text('Disease: ${props['disease']}', style: const TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
            Text('Severity: ${props['severity']}', style: const TextStyle(color: Colors.white70)),
            const SizedBox(height: 24),
            ElevatedButton(
              onPressed: () => Navigator.pop(ctx),
              style: ElevatedButton.styleFrom(backgroundColor: AppColors.accent, foregroundColor: Colors.black),
              child: const Center(child: Text('VIEW TREATMENT PLAN')),
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('REGIONAL DISEASE MAP'),
        backgroundColor: Colors.transparent,
        elevation: 0,
      ),
      extendBodyBehindAppBar: true,
      body: Stack(
        children: [
          FlutterMap(
            options: const MapOptions(
              initialCenter: LatLng(20.5937, 78.9629), // Center of India
              initialZoom: 5.0,
            ),
            children: [
              TileLayer(
                urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                userAgentPackageName: 'com.nukropai.app',
              ),
              MarkerLayer(markers: _markers),
            ],
          ),
          if (_isLoading)
            const Center(child: CircularProgressIndicator()),
          Positioned(
            bottom: 40,
            left: 20,
            right: 20,
            child: Container(
              padding: const EdgeInsets.all(16),
              decoration: AppColors.glassDecoration(radius: 20),
              child: const Row(
                children: [
                  Icon(Icons.info_outline, color: AppColors.accent),
                  SizedBox(width: 12),
                  Expanded(
                    child: Text(
                      'Live heatmaps generated from community reports and regional AI analytics.',
                      style: TextStyle(color: Colors.white70, fontSize: 11),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
