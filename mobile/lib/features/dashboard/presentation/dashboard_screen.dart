import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import 'package:intl/intl.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/l10n/app_localizations.dart';
import '../../auth/data/auth_repository.dart';
import '../../scanner/data/scanner_repository.dart';
import '../../scanner/presentation/scanner_screen.dart';
import 'settings_screen.dart';
import 'history_screen.dart';
import 'recommendations_screen.dart';
import '../../../core/api/scanner_service.dart';
import '../../../core/api/connectivity_service.dart';
import '../../chat/presentation/chat_screen.dart';

class DashboardScreen extends ConsumerStatefulWidget {
  const DashboardScreen({super.key});

  @override
  ConsumerState<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends ConsumerState<DashboardScreen> {
  Future<void> _refresh() async {
    ref.invalidate(scanHistoryProvider);
    ref.invalidate(currentWeatherProvider);
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final l10n = AppLocalizations.of(context) ?? AppLocalizations.instance;
    final weatherAsync = ref.watch(currentWeatherProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // Premium Blurred Background
          Positioned.fill(
            child: Container(
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topLeft,
                  end: Alignment.bottomRight,
                  colors: [
                    Color(0xFF0F172A),
                    Color(0xFF1E1B4B),
                    Color(0xFF312E81),
                  ],
                ),
              ),
            ),
          ),
          
          // Decorative background elements
          Positioned(
            top: -100,
            right: -100,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: AppColors.accent.withOpacity(0.05),
              ),
            ),
          ),

          RefreshIndicator(
            onRefresh: _refresh,
            color: AppColors.accent,
            backgroundColor: AppColors.background,
            child: CustomScrollView(
              physics: const BouncingScrollPhysics(parent: AlwaysScrollableScrollPhysics()),
              slivers: [
                SliverAppBar(
                  expandedHeight: 140,
                  floating: true,
                  pinned: true,
                  elevation: 0,
                  backgroundColor: Colors.transparent,
                  flexibleSpace: FlexibleSpaceBar(
                    background: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 24),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.end,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text('NUKROPAI INTELLIGENCE', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 10, letterSpacing: 4)),
                          const SizedBox(height: 4),
                          Text(user?.displayName ?? 'Hello, Farmer', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 28, letterSpacing: -1)),
                        ],
                      ),
                    ),
                  ),
                  actions: [
                    _buildGlassActionIcon(Icons.settings_rounded, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen()))),
                    const SizedBox(width: 16),
                  ],
                ),
                SliverToBoxAdapter(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(height: 10),
                        
                        // Real-Time Weather (Advanced Glass)
                        weatherAsync.when(
                          data: (weather) => _buildAdvancedWeatherCard(context, weather),
                          loading: () => _buildAdvancedWeatherCard(context, {'temp': '...', 'condition': 'Syncing', 'location': 'GPS Locating'}),
                          error: (err, __) => _buildAdvancedWeatherCard(context, {'temp': '!', 'condition': 'Offline', 'location': 'Check Connection'}),
                        ),

                        const SizedBox(height: 32),
                        
                        _buildSectionTitle('AI DIAGNOSTICS'),
                        const SizedBox(height: 16),
                        _buildGlassActionGrid(context, l10n),
                        
                        const SizedBox(height: 32),
                        
                        _buildSectionTitle('SMART ASSISTANT'),
                        const SizedBox(height: 16),
                        _buildGlassChatBanner(context),

                        const SizedBox(height: 32),
                        
                        _buildSectionTitle('ENVIRONMENTAL INSIGHTS'),
                        const SizedBox(height: 16),
                        _buildGlassContextSection(context),

                        const SizedBox(height: 120),
                      ],
                    ),
                  ),
                ),
              ],
            ),
          ),
          
          // Fixed Bottom Navigation (Glass)
          Positioned(
            bottom: 30,
            left: 24,
            right: 24,
            child: _buildGlassBottomNav(context, l10n),
          ),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return FadeInLeft(
      child: Text(
        title,
        style: const TextStyle(
          color: Colors.white70,
          fontWeight: FontWeight.bold,
          fontSize: 12,
          letterSpacing: 2,
        ),
      ),
    );
  }

  Widget _buildGlassActionIcon(IconData icon, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        margin: const EdgeInsets.only(top: 8),
        padding: const EdgeInsets.all(10),
        decoration: AppColors.glassDecoration(radius: 12),
        child: Icon(icon, color: Colors.white, size: 20),
      ),
    );
  }

  Widget _buildAdvancedWeatherCard(BuildContext context, Map<String, dynamic> weather) {
    final temp = weather['temp']?.toString() ?? '--';
    final condition = weather['condition'] ?? 'Unknown';
    final location = weather['location'] ?? 'Locating...';
    final iconData = weather['icon'] as IconData? ?? Icons.wb_sunny_rounded;

    return ZoomIn(
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: AppColors.glassDecoration(radius: 32, highlight: true),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(location, style: const TextStyle(color: Colors.white70, fontSize: 13, fontWeight: FontWeight.w500)),
                    const SizedBox(height: 4),
                    Text(condition.toUpperCase(), style: const TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.w900, letterSpacing: 1)),
                  ],
                ),
                Icon(iconData, color: AppColors.accent, size: 48),
              ],
            ),
            const SizedBox(height: 32),
            Row(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(temp, style: const TextStyle(color: Colors.white, fontSize: 72, fontWeight: FontWeight.bold, height: 0.8)),
                const Padding(
                  padding: EdgeInsets.only(bottom: 12, left: 4),
                  child: Text('°C', style: TextStyle(color: AppColors.accent, fontSize: 24, fontWeight: FontWeight.bold)),
                ),
                const Spacer(),
                _glassWeatherStat(Icons.water_drop_rounded, '${weather['humidity'] ?? '--'}%', 'Humidity'),
                const SizedBox(width: 24),
                _glassWeatherStat(Icons.air_rounded, '${weather['windSpeed'] ?? '--'} km/h', 'Wind'),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _glassWeatherStat(IconData icon, String value, String label) {
    return Column(
      children: [
        Icon(icon, color: Colors.white70, size: 18),
        const SizedBox(height: 4),
        Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
        Text(label, style: const TextStyle(color: Colors.white38, fontSize: 10, fontWeight: FontWeight.bold)),
      ],
    );
  }

  Widget _buildGlassActionGrid(BuildContext context, AppLocalizations l10n) {
    return GridView.count(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      crossAxisCount: 2,
      mainAxisSpacing: 16,
      crossAxisSpacing: 16,
      childAspectRatio: 1.2,
      children: [
        _glassActionCard('CROP SCAN', Icons.qr_code_scanner_rounded, AppColors.accent, () => _openScanner(context, false)),
        _glassActionCard('SOIL TEST', Icons.layers_rounded, Colors.orangeAccent, () => _openScanner(context, true)),
        _glassActionCard('RECORDS', Icons.history_rounded, Colors.blueAccent, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const HistoryScreen()))),
        _glassActionCard('EXPERT TIPS', Icons.lightbulb_rounded, Colors.amberAccent, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const RecommendationsScreen()))),
      ],
    );
  }

  Widget _glassActionCard(String title, IconData icon, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: AppColors.glassDecoration(radius: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Icon(icon, color: color, size: 32),
            Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 13, letterSpacing: 1)),
          ],
        ),
      ),
    );
  }

  Widget _buildGlassChatBanner(BuildContext context) {
    return GestureDetector(
      onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ChatScreen())),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: AppColors.glassDecoration(radius: 24),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: AppColors.accent.withOpacity(0.2), shape: BoxShape.circle),
              child: const Icon(Icons.auto_awesome, color: AppColors.accent, size: 24),
            ),
            const SizedBox(width: 16),
            const Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('On-Device AI Assistant', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                  Text('Active & Offline Ready', style: TextStyle(color: Colors.white38, fontSize: 11, fontWeight: FontWeight.bold)),
                ],
              ),
            ),
            const Icon(Icons.arrow_forward_ios_rounded, color: Colors.white24, size: 16),
          ],
        ),
      ),
    );
  }

  Widget _buildGlassContextSection(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 32),
      child: Column(
        children: [
          _glassContextItem(Icons.wb_sunny_rounded, 'Sunrise', '05:42 AM', Colors.orange),
          const SizedBox(height: 16),
          _glassContextItem(Icons.water_drop_rounded, 'Dew Point', '18°C', Colors.blue),
          const SizedBox(height: 16),
          _glassContextItem(Icons.wb_twilight_rounded, 'Sunset', '07:12 PM', Colors.deepOrange),
        ],
      ),
    );
  }

  Widget _glassContextItem(IconData icon, String label, String value, Color color) {
    return Row(
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(width: 16),
        Text(label, style: const TextStyle(color: Colors.white60, fontSize: 14, fontWeight: FontWeight.w500)),
        const Spacer(),
        Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
      ],
    );
  }

  Widget _buildGlassBottomNav(BuildContext context, AppLocalizations l10n) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      decoration: AppColors.glassDecoration(radius: 40, highlight: true),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _navItem(Icons.grid_view_rounded, true),
          _navItem(Icons.analytics_rounded, false),
          GestureDetector(
            onTap: () => _openScanner(context, false),
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 12),
              decoration: BoxDecoration(color: AppColors.accent, borderRadius: BorderRadius.circular(30)),
              child: const Row(
                children: [
                  Icon(Icons.add_a_photo_rounded, color: Colors.white, size: 20),
                  SizedBox(width: 8),
                  Text('SCAN', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 1)),
                ],
              ),
            ),
          ),
          _navItem(Icons.history_rounded, false),
          _navItem(Icons.person_rounded, false),
        ],
      ),
    );
  }

  Widget _navItem(IconData icon, bool active) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12),
      child: Icon(icon, color: active ? AppColors.accent : Colors.white38, size: 24),
    );
  }

  void _openScanner(BuildContext context, bool isSoil) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => ScannerScreen(isSoil: isSoil)));
  }
}
