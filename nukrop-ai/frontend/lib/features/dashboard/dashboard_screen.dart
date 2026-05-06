import 'package:flutter/material.dart';
import 'package:lucide_icons/lucide_icons.dart';
import 'package:nukrop_ai/core/local_sync.dart';
import 'package:nukrop_ai/features/voice_ai/voice_companion_screen.dart';
import 'package:nukrop_ai/features/scanner/video_scan_screen.dart';

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    double health = LocalFarmEngine.getOverallHealth();

    return Scaffold(
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text("Krishi Dashboard 🚀", style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.white)),
                  CircleAvatar(backgroundColor: Colors.white10, child: const Icon(LucideIcons.bell, color: Colors.white)),
                ],
              ),
              const SizedBox(height: 30),

              // Feature 6: GAMIFIED FARM HEALTH SCORE WIDGET
              Container(
                padding: const EdgeInsets.all(24),
                decoration: BoxDecoration(
                  gradient: const LinearGradient(colors: [Color(0xFF0FCE7D), Color(0xFF0B9C5D)]),
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [BoxShadow(color: const Color(0xFF0FCE7D).withOpacity(0.3), blurRadius: 12, offset: const Offset(0,8))]
                ),
                child: Column(
                  children: [
                    const Text("FARM HEALTH", style: TextStyle(letterSpacing: 2, color: Colors.white70, fontSize: 12)),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      crossAxisAlignment: CrossAxisAlignment.baseline,
                      textBaseline: TextBaseline.alphabetic,
                      children: [
                        Text("${health.toInt()}", style: const TextStyle(fontSize: 68, fontWeight: FontWeight.bold, color: Colors.white)),
                        const Text("%", style: TextStyle(fontSize: 32, color: Colors.white70)),
                      ],
                    ),
                    const SizedBox(height: 15),
                    const Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      children: [
                        Text("💧 Water: 60%", style: TextStyle(color: Colors.white)),
                        Text("🌱 Soil: 70%", style: TextStyle(color: Colors.white)),
                        Text("🌾 Crop: 80%", style: TextStyle(color: Colors.white)),
                      ],
                    )
                  ],
                ),
              ),

              const SizedBox(height: 30),
              const Text("Operating System Capabilities", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.grey)),
              const SizedBox(height: 15),

              GridView.count(
                shrinkWrap: true,
                physics: const NeverScrollableScrollPhysics(),
                crossAxisCount: 2,
                crossAxisSpacing: 15, mainAxisSpacing: 15, childAspectRatio: 0.9,
                children: [
                  _OSCard("AI Video\nCrop Scan", LucideIcons.camera, const Color(0xFF3B82F6), () {
                    Navigator.push(context, MaterialPageRoute(builder: (_) => const VideoScanScreen()));
                  }),
                  _OSCard("Rural Voice\nCompanion", LucideIcons.mic, const Color(0xFFF59E0B), () {
                     Navigator.push(context, MaterialPageRoute(builder: (_) => const VoiceCompanionScreen()));
                  }),
                  _OSCard("Yield Market\nPredictor", LucideIcons.trendingUp, const Color(0xFF8B5CF6), (){}),
                  _OSCard("Emergency\nThreat Alerts", LucideIcons.alertTriangle, const Color(0xFFEF4444), (){}),
                ],
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _OSCard(String title, IconData icon, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: const Color(0xFF1E293B), borderRadius: BorderRadius.circular(20), border: Border.all(color: color.withOpacity(0.3))),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: color.withOpacity(0.15), shape: BoxShape.circle), child: Icon(icon, color: color)),
            const Spacer(),
            Text(title, style: const TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.w600, height: 1.2)),
          ],
        ),
      ),
    );
  }
}