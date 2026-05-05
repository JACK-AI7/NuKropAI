import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/l10n/locale_provider.dart';
import '../../auth/data/auth_repository.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/config/constants.dart';
import '../../../core/api/server_config.dart';
import 'dart:ui';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  final TextEditingController _serverController = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadServerUrl();
  }

  Future<void> _loadServerUrl() async {
    final prefs = await SharedPreferences.getInstance();
    final savedUrl = prefs.getString('server_url') ?? AppConstants.baseUrl;
    _serverController.text = savedUrl;
  }

  Future<void> _saveServerUrl() async {
    final url = _serverController.text.trim();
    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Please enter a valid URL starting with http:// or https://'), backgroundColor: Colors.red),
        );
      }
      return;
    }

    final config = ref.read(serverConfigProvider);
    await config.saveServerUrl(url);
    ref.read(serverUrlProvider.notifier).state = url;
    
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Server URL updated!'), backgroundColor: Colors.green),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    final currentLocale = ref.watch(localeProvider);

    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Stack(
        children: [
          // Background Glow
          Positioned(
            bottom: -100,
            right: -100,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                color: AppColors.accent.withOpacity(0.05),
                shape: BoxShape.circle,
              ),
              child: BackdropFilter(filter: ImageFilter.blur(sigmaX: 60, sigmaY: 60), child: Container()),
            ),
          ),

          CustomScrollView(
            physics: const BouncingScrollPhysics(),
            slivers: [
              SliverAppBar(
                expandedHeight: 120,
                pinned: true,
                backgroundColor: Colors.transparent,
                elevation: 0,
                flexibleSpace: const FlexibleSpaceBar(
                  centerTitle: true,
                  title: Text('SETTINGS', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 14, letterSpacing: 3)),
                ),
                leading: Container(
                  margin: const EdgeInsets.all(8),
                  decoration: AppColors.glassDecoration(radius: 12),
                  child: IconButton(
                    icon: const Icon(Icons.arrow_back_ios_new_rounded, color: Colors.white, size: 18),
                    onPressed: () => Navigator.pop(context),
                  ),
                ),
              ),
              
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildSectionTitle('PREFERENCES'),
                      const SizedBox(height: 16),
                      _buildGlassSettingTile(
                        'Language', 
                        'Choose app language', 
                        Icons.translate_rounded, 
                        trailing: DropdownButton<String>(
                          value: currentLocale.languageCode,
                          dropdownColor: const Color(0xFF1E293B),
                          style: const TextStyle(color: Colors.white, fontSize: 13, fontWeight: FontWeight.bold),
                          underline: const SizedBox(),
                          onChanged: (val) => ref.read(localeProvider.notifier).setLocale(val!),
                          items: const [
                            DropdownMenuItem(value: 'en', child: Text('🇬🇧 English')),
                            DropdownMenuItem(value: 'hi', child: Text('🇮🇳 हिंदी')),
                            DropdownMenuItem(value: 'te', child: Text('🇮🇳 తెలుగు')),
                          ],
                        ),
                      ),
                      
                      const SizedBox(height: 32),
                      _buildSectionTitle('CONNECTIVITY'),
                      const SizedBox(height: 16),
                      _buildGlassServerConfig(),
                      
                      const SizedBox(height: 32),
                      _buildSectionTitle('ABOUT'),
                      const SizedBox(height: 16),
                      _buildGlassSettingTile('Help Center', 'FAQs and troubleshooting', Icons.help_outline_rounded),
                      const SizedBox(height: 12),
                      _buildGlassSettingTile('Privacy Policy', 'How we use your data', Icons.privacy_tip_outlined),
                      const SizedBox(height: 12),
                      _buildGlassSettingTile('App Version', 'Build 1.0.42-stable', Icons.info_outline_rounded, trailing: const Text('v1.0.4', style: TextStyle(color: Colors.white24, fontSize: 12))),
                      
                      const SizedBox(height: 64),
                      _buildGlassSignOutButton(),
                      const SizedBox(height: 100),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Padding(
      padding: const EdgeInsets.only(left: 4),
      child: Text(title, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.w900, color: Colors.white38, letterSpacing: 2)),
    );
  }

  Widget _buildGlassSettingTile(String title, String subtitle, IconData icon, {Widget? trailing}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: AppColors.glassDecoration(radius: 24),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: Colors.white.withOpacity(0.05), borderRadius: BorderRadius.circular(12)),
            child: Icon(icon, color: AppColors.accent, size: 20),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 15)),
                Text(subtitle, style: const TextStyle(color: Colors.white38, fontSize: 11)),
              ],
            ),
          ),
          trailing ?? const Icon(Icons.chevron_right_rounded, color: Colors.white24),
        ],
      ),
    );
  }

  Widget _buildGlassServerConfig() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 28),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.dns_rounded, color: Colors.blueAccent, size: 20),
              const SizedBox(width: 12),
              const Text('Backend URL', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
              const Spacer(),
              GestureDetector(
                onTap: _saveServerUrl,
                child: const Text('SAVE', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 12)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _serverController,
            style: const TextStyle(color: Colors.white, fontSize: 14),
            decoration: InputDecoration(
              hintText: 'http://your-ip:3000/api',
              hintStyle: const TextStyle(color: Colors.white24, fontSize: 12),
              filled: true,
              fillColor: Colors.white.withOpacity(0.03),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            ),
          ),
          const SizedBox(height: 12),
          const Text('Requires app restart after saving to take full effect.', style: TextStyle(color: Colors.white24, fontSize: 10, fontStyle: FontStyle.italic)),
        ],
      ),
    );
  }

  Widget _buildGlassSignOutButton() {
    return Center(
      child: GestureDetector(
        onTap: () async {
          final confirmed = await showDialog<bool>(
            context: context,
            builder: (ctx) => AlertDialog(
              backgroundColor: const Color(0xFF1E293B),
              title: const Text('Sign Out', style: TextStyle(color: Colors.white)),
              content: const Text('Are you sure you want to exit NuKropAI?', style: TextStyle(color: Colors.white70)),
              actions: [
                TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
                TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Sign Out', style: TextStyle(color: Colors.redAccent))),
              ],
            ),
          );
          if (confirmed == true) {
            await ref.read(authProvider.notifier).logout();
            if (mounted) Navigator.of(context).popUntil((route) => route.isFirst);
          }
        },
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 48, vertical: 18),
          decoration: AppColors.glassDecoration(radius: 30, highlight: true),
          child: const Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.logout_rounded, color: Colors.redAccent, size: 20),
              SizedBox(width: 12),
              Text('SIGN OUT', style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 12, letterSpacing: 1.5)),
            ],
          ),
        ),
      ),
    );
  }
}
