import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/l10n/locale_provider.dart';
import '../../auth/data/auth_repository.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../../core/config/constants.dart';
import '../../../core/api/server_config.dart';

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
    final ref = this.ref;
    final currentLocale = ref.watch(localeProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Settings', style: TextStyle(fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: AppColors.textPrimary),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildSectionTitle('App Preferences'),
            const SizedBox(height: 16),
            _buildSettingTile(
              context, 
              'Language', 
              'Choose your preferred language', 
              Icons.translate_rounded, 
              trailing: DropdownButton<String>(
                value: currentLocale.languageCode,
                underline: const SizedBox(),
                onChanged: (val) => ref.read(localeProvider.notifier).setLocale(val!),
                items: const [
                  DropdownMenuItem(value: 'en', child: Text('🇬🇧 English')),
                  DropdownMenuItem(value: 'hi', child: Text('🇮🇳 हिंदी')),
                  DropdownMenuItem(value: 'te', child: Text('🇮🇳 తెలుగు')),
                ],
              ),
            ),
            const SizedBox(height: 16),
            _buildSettingTile(
              context, 
              'Server Address', 
              'Set backend IP (e.g. http://192.168.1.5:3000/api)', 
              Icons.dns_rounded, 
              trailing: IconButton(
                icon: const Icon(Icons.save_rounded, color: AppColors.primary),
                onPressed: _saveServerUrl,
              ),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 8),
              child: TextField(
                controller: _serverController,
                decoration: InputDecoration(
                  hintText: 'http://YOUR_IP:3000/api',
                  hintStyle: const TextStyle(fontSize: 12),
                  filled: true,
                  fillColor: Colors.white,
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(12), borderSide: BorderSide.none),
                ),
                style: const TextStyle(fontSize: 13),
              ),
            ),
            const SizedBox(height: 40),
            _buildSectionTitle('Support'),
            const SizedBox(height: 16),
            _buildSettingTile(context, 'Help Center', 'FAQs and troubleshooting', Icons.help_outline),
            const SizedBox(height: 16),
            _buildSettingTile(context, 'Privacy Policy', 'How we use your data', Icons.privacy_tip_outlined),
            const SizedBox(height: 60),
            // Sign Out Button
            Center(
              child: ElevatedButton.icon(
                onPressed: () async {
                  final confirmed = await showDialog<bool>(
                    context: context,
                    builder: (ctx) => AlertDialog(
                      title: const Text('Sign Out'),
                      content: const Text('Are you sure you want to sign out?'),
                      actions: [
                        TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
                        TextButton(onPressed: () => Navigator.pop(ctx, true), child: const Text('Sign Out')),
                      ],
                    ),
                  );
                  if (confirmed == true) {
                    await ref.read(authProvider.notifier).logout();
                    if (mounted) {
                      Navigator.of(context).popUntil((route) => route.isFirst);
                    }
                  }
                },
                icon: const Icon(Icons.logout, color: Colors.white),
                label: const Text('Sign Out', style: TextStyle(color: Colors.white)),
                style: ElevatedButton.styleFrom(
                  backgroundColor: Colors.red,
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(30)),
                ),
              ),
            ),
            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppColors.textSecondary, letterSpacing: 1));
  }

  Widget _buildSettingTile(BuildContext context, String title, String subtitle, IconData icon, {Widget? trailing}) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.02), blurRadius: 10, offset: const Offset(0, 4))],
      ),
      child: Row(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: AppColors.background, borderRadius: BorderRadius.circular(12)),
            child: Icon(icon, color: AppColors.primary, size: 20),
          ),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
                Text(subtitle, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12)),
              ],
            ),
          ),
          trailing ?? const Icon(Icons.chevron_right, color: AppColors.textSecondary),
        ],
      ),
    );
  }
}
