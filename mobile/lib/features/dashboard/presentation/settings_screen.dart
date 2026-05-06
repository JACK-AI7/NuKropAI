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
import '../../../core/ai/llm_service.dart';
import 'ai_health_screen.dart';

class SettingsScreen extends ConsumerStatefulWidget {
  const SettingsScreen({super.key});

  @override
  ConsumerState<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends ConsumerState<SettingsScreen> {
  final TextEditingController _serverController = TextEditingController();
  final TextEditingController _apiKeyController = TextEditingController();
  bool _apiKeyVisible = false;
  String _selectedModel = 'gemini-1.5-flash';

  @override
  void initState() {
    super.initState();
    _loadServerUrl();
    _loadApiKey();
    _loadModel();
  }

  Future<void> _loadApiKey() async {
    final prefs = await SharedPreferences.getInstance();
    _apiKeyController.text = prefs.getString('gemini_api_key') ?? '';
  }

  Future<void> _loadModel() async {
    final prefs = await SharedPreferences.getInstance();
     setState(() {
       _selectedModel = prefs.getString('gemini_model') ?? 'gemini-1.5-flash';
     });
  }

  Future<void> _saveApiKey() async {
    final key = _apiKeyController.text.trim();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('gemini_api_key', key);
    // Update LLM service with new key
    final llmService = LLMService();
    await llmService.updateApiKey(key);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('API Key saved!'), backgroundColor: Colors.green),
      );
    }
  }

  Future<void> _saveModel() async {
    final llmService = LLMService();
    await llmService.updateModel(_selectedModel);
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Model updated to ${_getModelDisplayName(_selectedModel)}'), backgroundColor: Colors.green),
      );
    }
  }

  String _getModelDisplayName(String modelValue) {
    final displayName = LLMService.geminiModels.entries
        .firstWhere((e) => e.value == modelValue, orElse: () => const MapEntry('Unknown', 'unknown'))
        .key;
    return displayName;
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
                      _buildSectionTitle('AI MODEL CONFIGURATION'),
                      const SizedBox(height: 16),
                      _buildGlassModelConfig(),
                      const SizedBox(height: 24),
                      _buildGeminiApiConfig(),
                      
                       const SizedBox(height: 32),
                      _buildSectionTitle('SYSTEM STATUS'),
                      const SizedBox(height: 16),
                      GestureDetector(
                        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AIHealthScreen())),
                        child: _buildGlassSettingTile('AI Engine Health', 'Monitor Hugging Face Space status', Icons.health_and_safety_rounded),
                      ),
                      
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

  Widget _buildGlassModelConfig() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 28),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.smart_toy_rounded, color: Colors.deepPurpleAccent, size: 20),
              const SizedBox(width: 12),
              const Text('AI Model', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
              const Spacer(),
              GestureDetector(
                onTap: _saveModel,
                child: const Text('SAVE', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 12)),
              ),
            ],
          ),
          const SizedBox(height: 16),
          DropdownButtonFormField<String>(
            initialValue: _selectedModel,
            dropdownColor: const Color(0xFF1E293B),
            style: const TextStyle(color: Colors.white, fontSize: 14),
            decoration: InputDecoration(
              hintText: 'Select AI model',
              hintStyle: const TextStyle(color: Colors.white24, fontSize: 12),
              filled: true,
              fillColor: Colors.white.withOpacity(0.03),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            ),
            items: LLMService.geminiModels.entries.map((entry) {
              return DropdownMenuItem<String>(
                value: entry.value,
                child: Text(entry.key, style: const TextStyle(fontSize: 13)),
              );
            }).toList(),
            onChanged: (value) {
              setState(() {
                _selectedModel = value!;
              });
            },
          ),
          const SizedBox(height: 12),
          const Text(
            'Agricultural AI Models: AgriChat, AgriGPT-VL, AgriM-LLM, Agri-LLaVA, CropSeek-LLM.\nGeneral Models: Llama 3.2 Vision, Qwen 2.5 VL, Phi-4 Multimodal.',
            style: TextStyle(color: Colors.white24, fontSize: 10, fontStyle: FontStyle.italic),
          ),
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
              hintText: 'http://your-ip:3000',
              hintStyle: const TextStyle(color: Colors.white24, fontSize: 12),
              filled: true,
              fillColor: Colors.white.withOpacity(0.03),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
            ),
          ),
          const SizedBox(height: 12),
          const Text('Optional: only needed for cloud sync. App works without it.', style: TextStyle(color: Colors.white24, fontSize: 10, fontStyle: FontStyle.italic)),
        ],
      ),
    );
  }

  Widget _buildGeminiApiConfig() {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 28),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.psychology_rounded, color: Colors.deepPurpleAccent, size: 20),
              const SizedBox(width: 12),
              const Text('Gemini API Key', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
              const Spacer(),
              GestureDetector(
                onTap: _saveApiKey,
                child: const Text('SAVE', style: TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 12)),
              ),
            ],
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _apiKeyController,
            obscureText: !_apiKeyVisible,
            style: const TextStyle(color: Colors.white, fontSize: 14),
            decoration: InputDecoration(
              hintText: 'AIzaSy...',
              hintStyle: const TextStyle(color: Colors.white24, fontSize: 12),
              filled: true,
              fillColor: Colors.white.withOpacity(0.03),
              border: OutlineInputBorder(borderRadius: BorderRadius.circular(16), borderSide: BorderSide.none),
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              suffixIcon: IconButton(
                icon: Icon(_apiKeyVisible ? Icons.visibility_off : Icons.visibility, color: Colors.white38, size: 18),
                onPressed: () => setState(() => _apiKeyVisible = !_apiKeyVisible),
              ),
            ),
          ),
          const SizedBox(height: 12),
          const Text('Get a free key from Google AI Studio. Enables detailed AI analysis. Leave empty to use on-device only.', style: TextStyle(color: Colors.white24, fontSize: 10, fontStyle: FontStyle.italic)),
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

