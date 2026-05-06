import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import '../../../core/theme/app_theme.dart';

class DiseaseMapScreen extends StatefulWidget {
  const DiseaseMapScreen({super.key});

  @override
  State<DiseaseMapScreen> createState() => _DiseaseMapScreenState();
}

class _DiseaseMapScreenState extends State<DiseaseMapScreen> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Disease Map'),
        backgroundColor: AppColors.primary,
      ),
      body: FlutterMap(
        options: const MapOptions(
          initialCenter: LatLng(20.5937, 78.9629), // India center
          initialZoom: 5,
        ),
        children: [
          TileLayer(
            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            userAgentPackageName: 'com.example.nukropai',
          ),
          // Add markers for disease hotspots here
        ],
      ),
    );
  }
}