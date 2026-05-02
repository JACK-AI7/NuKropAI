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
    final ref = this.ref;
    final authState = ref.watch(authProvider);
    final user = authState.user;
    final l10n = AppLocalizations.of(context) ?? AppLocalizations.instance;

    // Weather from provider (live)
    final weatherAsync = ref.watch(currentWeatherProvider);

    return Scaffold(
      body: Stack(
        children: [
          // Background Image
          Positioned.fill(
            child: Image.network(
              'https://images.unsplash.com/photo-1500382017468-9049fed747ef?q=80&w=2000',
              fit: BoxFit.cover,
            ),
          ),
          // Dark Overlay
          Positioned.fill(
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    Colors.black.withOpacity(0.4),
                    Colors.black.withOpacity(0.8),
                  ],
                ),
              ),
            ),
          ),

          RefreshIndicator(
            onRefresh: _refresh,
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 20),
                  _buildTopBar(context, ref),
                  const SizedBox(height: 30),

                  // Weather Widget (Live)
                  weatherAsync.when(
                    data: (weather) => _buildMinimalistWeatherCard(context, weather),
                    loading: () => _buildMinimalistWeatherCard(context, {
                      'temp': '--',
                      'condition': 'Loading...',
                      'location': 'Current Location',
                      'humidity': '--',
                      'windSpeed': '--',
                      'icon': Icons.cloud,
                    }),
                    error: (_, __) => _buildMinimalistWeatherCard(context, {
                      'temp': '--',
                      'condition': 'Unavailable',
                      'location': 'Enable GPS',
                      'humidity': '--',
                      'windSpeed': '--',
                      'icon': Icons.location_off,
                    }),
                  ),

                  const SizedBox(height: 30),

                  // Smart Context
                  _buildMinimalistContextSection(context),

                  const SizedBox(height: 40),

                  // Action Grid
                  Text(l10n.quickActions, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white)),
                  const SizedBox(height: 20),
                  _buildGlassActionGrid(context, l10n),

                  const SizedBox(height: 100),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildTopBar(BuildContext context, WidgetRef ref) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('NUKROPAI', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 12, letterSpacing: 3)),
            Text('Ludhiana, Punjab', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
          ],
        ),
        GestureDetector(
          onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const SettingsScreen())),
          child: Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.white.withOpacity(0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.white.withOpacity(0.2)),
            ),
            child: const Icon(Icons.grid_view_rounded, color: Colors.white, size: 20),
          ),
        ),
      ],
    );
  }

  Widget _buildMinimalistWeatherCard(BuildContext context, Map<String, dynamic> weather) {
    final temp = weather['temp']?.toString() ?? '--';
    final condition = weather['condition'] ?? 'Unknown';
    final location = weather['location'] ?? 'Current Location';
    final iconData = weather['icon'] as IconData? ?? Icons.cloud;

    return FadeInDown(
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(32),
        ),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(location, style: const TextStyle(color: AppColors.textGrey, fontWeight: FontWeight.w600, fontSize: 14)),
                    const SizedBox(height: 4),
                    Text(DateFormat('EEEE, MMMM d').format(DateTime.now()), style: const TextStyle(color: AppColors.textDark, fontWeight: FontWeight.bold, fontSize: 12)),
                  ],
                ),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                  decoration: BoxDecoration(color: AppColors.offWhite, borderRadius: BorderRadius.circular(20)),
                  child: Row(
                    children: [
                      Icon(iconData, size: 16, color: AppColors.textDark),
                      const SizedBox(width: 4),
                      Text(condition, style: const TextStyle(color: AppColors.textDark, fontWeight: FontWeight.bold, fontSize: 10)),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('${temp}°C', style: const TextStyle(color: AppColors.textDark, fontSize: 64, fontWeight: FontWeight.w900, letterSpacing: -2)),
                const Spacer(),
                Column(
                  children: [
                    _weatherSmallTag('H: ${weather['humidity'] ?? 65}%'),
                    const SizedBox(height: 8),
                    _weatherSmallTag('W: ${weather['windSpeed'] ?? 12}km/h'),
                  ],
                )
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _weatherSmallTag(String text) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(color: AppColors.offWhite, borderRadius: BorderRadius.circular(8)),
      child: Text(text, style: const TextStyle(color: AppColors.textDark, fontWeight: FontWeight.bold, fontSize: 10)),
    );
  }

  Widget _buildMinimalistContextSection(BuildContext context) {
    return FadeInUp(
      delay: const Duration(milliseconds: 200),
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.9),
          borderRadius: BorderRadius.circular(28),
        ),
        child: Column(
          children: [
            _contextItem(Icons.wb_sunny_rounded, 'Today Sunrise', '05:42 AM', Colors.orange),
            const Divider(height: 24, color: AppColors.offWhite),
            _contextItem(Icons.auto_awesome_rounded, 'Golden Hour', '06:15 AM - 07:15 AM', Colors.amber),
            const Divider(height: 24, color: AppColors.offWhite),
            _contextItem(Icons.wb_twilight_rounded, 'Today Sunset', '07:12 PM', Colors.deepOrange),
          ],
        ),
      ),
    );
  }

  Widget _contextItem(IconData icon, String label, String value, Color color) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
          child: Icon(icon, color: color, size: 18),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: const TextStyle(color: AppColors.textGrey, fontWeight: FontWeight.w600, fontSize: 13)),
              const SizedBox(height: 2),
              Text(value, style: const TextStyle(color: AppColors.textDark, fontWeight: FontWeight.bold, fontSize: 14)),
            ],
          ),
        ),
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
      childAspectRatio: 1.1,
      children: [
        _glassCard(l10n.scanCrop, Icons.camera_rounded, AppColors.accent, () => _openScanner(context, false)),
        _glassCard(l10n.soilAnalysis, Icons.landslide_rounded, Colors.orangeAccent, () => _openScanner(context, true)),
        _glassCard(l10n.recommendations, Icons.auto_awesome_rounded, Colors.purpleAccent, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const RecommendationsScreen()))),
        _glassCard(l10n.history, Icons.history_rounded, Colors.blueGrey, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const HistoryScreen()))),
      ],
    );
  }

  Widget _glassCard(String title, IconData icon, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.white.withOpacity(0.1),
          borderRadius: BorderRadius.circular(24),
          border: Border.all(color: Colors.white.withOpacity(0.1)),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              padding: const EdgeInsets.all(10),
              decoration: BoxDecoration(color: color.withOpacity(0.2), shape: BoxShape.circle),
              child: Icon(icon, color: color, size: 24),
            ),
            Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
          ],
        ),
      ),
    );
  }

  Widget _buildScanFAB(BuildContext context, AppLocalizations l10n) {
    return FadeInUp(
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
        decoration: BoxDecoration(
          color: AppColors.accent,
          borderRadius: BorderRadius.circular(40),
          boxShadow: [BoxShadow(color: AppColors.accent.withOpacity(0.3), blurRadius: 20, offset: const Offset(0, 10))],
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.qr_code_scanner_rounded, color: Colors.white, size: 24),
            const SizedBox(width: 12),
            Text(l10n.scanButton, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, letterSpacing: 1.5)),
          ],
        ),
      ),
    );
  }

  void _openScanner(BuildContext context, bool isSoil) {
    Navigator.push(context, MaterialPageRoute(builder: (_) => ScannerScreen(isSoil: isSoil)));
  }
}
