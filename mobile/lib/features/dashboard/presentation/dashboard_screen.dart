import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';
import '../../auth/data/auth_repository.dart';
import '../../scanner/presentation/scanner_screen.dart';
import '../../chat/presentation/chat_screen.dart';
import '../../../core/api/scanner_service.dart';
import 'settings_screen.dart';
import 'dart:ui';
import 'disease_map_screen.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> with SingleTickerProviderStateMixin {
  late AnimationController _bgAnimationController;
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _bgAnimationController = AnimationController(
      vsync: this,
      duration: const Duration(seconds: 10),
    )..repeat(reverse: true);
  }

  @override
  void dispose() {
    _bgAnimationController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final weatherAsync = ref.watch(currentWeatherProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Stack(
        children: [
          // Dynamic Animated Background (Non-blocking)
          Positioned.fill(
            child: IgnorePointer(
              child: AnimatedBuilder(
                animation: _bgAnimationController,
                builder: (context, child) {
                  return Container(
                    decoration: BoxDecoration(
                      gradient: RadialGradient(
                        center: Alignment(
                          0.5 + 0.3 * _bgAnimationController.value,
                          0.5 + 0.2 * (1 - _bgAnimationController.value),
                        ),
                        radius: 1.5,
                        colors: const [
                          Color(0xFF1E293B),
                          Color(0xFF0F172A),
                        ],
                      ),
                    ),
                  );
                },
              ),
            ),
          ),
          
          // Floating Blurred Blobs (Non-blocking)
          Positioned(
            top: -50,
            right: -50,
            child: IgnorePointer(
              child: Container(
                width: 250,
                height: 250,
                decoration: BoxDecoration(
                  color: AppColors.accent.withOpacity(0.05),
                  shape: BoxShape.circle,
                ),
                child: BackdropFilter(filter: ImageFilter.blur(sigmaX: 50, sigmaY: 50), child: Container()),
              ),
            ),
          ),

          CustomScrollView(
            physics: const BouncingScrollPhysics(),
            slivers: [
              SliverAppBar(
                expandedHeight: 160,
                floating: true,
                pinned: true,
                elevation: 0,
                backgroundColor: Colors.transparent,
                flexibleSpace: FlexibleSpaceBar(
                  background: Container(
                    padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 32),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.end,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        FadeInLeft(
                          duration: const Duration(milliseconds: 800),
                          child: const Text('NUKROPAI INTELLIGENCE', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 11, letterSpacing: 3)),
                        ),
                        const SizedBox(height: 8),
                        FadeInUp(
                          duration: const Duration(milliseconds: 800),
                          child: Text(
                            user?['name'] ?? 'Hello, Farmer',
                            style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 32, letterSpacing: -1.5),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
                actions: [
                  Container(
                    margin: const EdgeInsets.only(right: 16),
                    decoration: AppColors.glassDecoration(radius: 14),
                    child: IconButton(
                      icon: const Icon(Icons.settings_outlined, color: Colors.white70),
                      onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen())),
                    ),
                  ),
                ],
              ),
              
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: Column(
                    children: [
                      const SizedBox(height: 12),
                      _buildAdvancedWeatherCard(weatherAsync),
                      const SizedBox(height: 32),
                      _buildActionGrid(),
                      const SizedBox(height: 32),
                      _buildAiAssistantBanner(),
                      const SizedBox(height: 40),
                      _buildSectionHeader('Recent Reports'),
                      const SizedBox(height: 16),
                      _buildRecentActivityList(),
                      const SizedBox(height: 140),
                    ],
                  ),
                ),
              ),
            ],
          ),

          // Enhanced Bottom Navigation Bar
          Positioned(
            bottom: 30,
            left: 24,
            right: 24,
            child: _buildGlassNavigationBar(),
          ),
        ],
      ),
    );
  }

  Widget _buildAdvancedWeatherCard(AsyncValue<Map<String, dynamic>> weatherAsync) {
    return weatherAsync.when(
      data: (weather) => FadeInDown(
        child: Container(
          width: double.infinity,
          padding: const EdgeInsets.all(28),
          decoration: AppColors.glassDecoration(radius: 36, highlight: true),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.location_on, color: AppColors.accent, size: 14),
                          const SizedBox(width: 4),
                          Text(weather['location'].toString().toUpperCase(), style: const TextStyle(color: Colors.white54, fontWeight: FontWeight.w900, fontSize: 10, letterSpacing: 1.5)),
                        ],
                      ),
                      const SizedBox(height: 4),
                      Text(weather['condition'], style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
                    ],
                  ),
                  Icon(weather['icon'] as IconData, color: Colors.white, size: 48),
                ],
              ),
              const SizedBox(height: 24),
              const Divider(color: Colors.white10),
              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: [
                  _weatherStat('Temp', '${weather['temp']}°C', Icons.thermostat),
                  _weatherStat('Humidity', '${weather['humidity']}%', Icons.water_drop),
                  _weatherStat('Wind', '${weather['windSpeed']}km/h', Icons.air),
                ],
              ),
            ],
          ),
        ),
      ),
      loading: () => Container(
        height: 180,
        decoration: AppColors.glassDecoration(radius: 36),
        child: const Center(child: CircularProgressIndicator(color: AppColors.accent)),
      ),
      error: (e, _) => Container(
        padding: const EdgeInsets.all(24),
        decoration: AppColors.glassDecoration(radius: 36),
        child: Column(
          children: [
            const Icon(Icons.cloud_off, color: Colors.white38, size: 32),
            const SizedBox(height: 12),
            const Text('Weather sync paused', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
            TextButton(
              onPressed: () => ref.refresh(currentWeatherProvider),
              child: const Text('RECONNECT', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 10)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _weatherStat(String label, String value, IconData icon) {
    return Column(
      children: [
        Icon(icon, color: AppColors.accent.withOpacity(0.6), size: 18),
        const SizedBox(height: 8),
        Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 16)),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(color: Colors.white38, fontSize: 10, fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildActionGrid() {
    return Row(
      children: [
        _actionCard('CROP SCAN', 'Identify diseases & pests', Icons.qr_code_scanner, AppColors.accent, () {
          Navigator.push(context, MaterialPageRoute(builder: (_) => const ScannerScreen(isSoil: false)));
        }),
        const SizedBox(width: 16),
        _actionCard('SOIL TEST', 'Analyze NPK & health', Icons.terrain_rounded, Colors.orangeAccent, () {
          Navigator.push(context, MaterialPageRoute(builder: (_) => const ScannerScreen(isSoil: true)));
        }),
      ],
    );
  }

  Widget _actionCard(String title, String subtitle, IconData icon, Color color, VoidCallback onTap) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Container(
          padding: const EdgeInsets.all(24),
          decoration: AppColors.glassDecoration(radius: 32),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
                child: Icon(icon, color: color, size: 28),
              ),
              const SizedBox(height: 20),
              Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 15, letterSpacing: 0.5)),
              const SizedBox(height: 4),
              Text(subtitle, style: const TextStyle(color: Colors.white38, fontSize: 11, height: 1.3)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildAiAssistantBanner() {
    return GestureDetector(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ChatScreen())),
      child: Container(
        width: double.infinity,
        padding: const EdgeInsets.all(24),
        decoration: AppColors.glassDecoration(radius: 32, highlight: true),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: const BoxDecoration(color: AppColors.accent, shape: BoxShape.circle),
              child: const Icon(Icons.auto_awesome, color: Colors.white, size: 24),
            ),
            const SizedBox(width: 20),
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('SMART ASSISTANT', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 15)),
                  SizedBox(height: 2),
                  Text('Ask anything about your crops', style: TextStyle(color: Colors.white54, fontSize: 12)),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios_rounded, color: Colors.white24, size: 16),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(title.toUpperCase(), style: const TextStyle(color: Colors.white54, fontWeight: FontWeight.w900, fontSize: 12, letterSpacing: 2)),
        const Text('View All', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold, fontSize: 12)),
      ],
    );
  }

  Widget _buildRecentActivityList() {
    return Column(
      children: List.generate(2, (index) => Container(
        margin: const EdgeInsets.only(bottom: 12),
        padding: const EdgeInsets.all(16),
        decoration: AppColors.glassDecoration(radius: 24),
        child: Row(
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(12),
              child: Container(width: 50, height: 50, color: Colors.white10, child: const Icon(Icons.eco, color: Colors.white24)),
            ),
            const SizedBox(width: 16),
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Apple Scab', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
                  Text('May 04, 2026', style: TextStyle(color: Colors.white38, fontSize: 11)),
                ],
              ),
            ),
            const Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text('HIGH', style: TextStyle(color: Colors.redAccent, fontWeight: FontWeight.w900, fontSize: 10)),
                Text('Severity', style: TextStyle(color: Colors.white24, fontSize: 9)),
              ],
            ),
          ],
          ),
        )),
    );
  }

  Widget _buildGlassNavigationBar() {
    return ClipRRect(
      borderRadius: BorderRadius.circular(40),
      child: BackdropFilter(
        filter: ImageFilter.blur(sigmaX: 20, sigmaY: 20),
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.08),
            borderRadius: BorderRadius.circular(40),
            border: Border.all(color: Colors.white.withOpacity(0.1)),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _navItem(0, Icons.grid_view_rounded),
              _navItem(1, Icons.history_rounded),
              _scanButton(),
              _navItem(2, Icons.insights_rounded, onTap: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => const DiseaseMapScreen()));
              }),
              _navItem(3, Icons.person_outline_rounded),
            ],
          ),
        ),
      ),
    );
  }

  Widget _navItem(int index, IconData icon, {VoidCallback? onTap}) {
    final active = _currentIndex == index;
    return GestureDetector(
      onTap: () {
        setState(() => _currentIndex = index);
        if (onTap != null) onTap();
      },
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: active ? BoxDecoration(color: AppColors.accent.withOpacity(0.2), shape: BoxShape.circle) : null,
        child: Icon(icon, color: active ? AppColors.accent : Colors.white38, size: 24),
      ),
    );
  }

  Widget _scanButton() {
    return GestureDetector(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ScannerScreen())),
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: const BoxDecoration(
          color: AppColors.accent,
          shape: BoxShape.circle,
          boxShadow: [BoxShadow(color: AppColors.accent, blurRadius: 15, spreadRadius: -5)],
        ),
        child: const Icon(Icons.add_a_photo_rounded, color: Colors.white, size: 28),
      ),
    );
  }
}
