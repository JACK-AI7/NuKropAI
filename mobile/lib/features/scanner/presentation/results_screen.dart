import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:animate_do/animate_do.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/api/server_config.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:cached_network_image/cached_network_image.dart';

IconData getWeatherIcon(int? code) {
  if (code == null) return Icons.cloud;
  if (code == 0) return Icons.wb_sunny;
  if (code >= 1 && code <= 3) return Icons.wb_cloudy;
  if (code >= 45 && code <= 48) return Icons.foggy;
  if (code >= 51 && code <= 67) return Icons.grain;
  if (code >= 71 && code <= 77) return Icons.ac_unit;
  if (code >= 80 && code <= 82) return Icons.umbrella;
  if (code >= 95 && code <= 99) return Icons.bolt;
  return Icons.cloud;
}

String getWeatherCondition(int? code) {
  if (code == null) return 'Unknown';
  if (code == 0) return 'Clear Sky';
  if (code >= 1 && code <= 3) return 'Partly Cloudy';
  if (code >= 45 && code <= 48) return 'Foggy';
  if (code >= 51 && code <= 67) return 'Rain';
  if (code >= 71 && code <= 77) return 'Snow';
  if (code >= 80 && code <= 82) return 'Showers';
  if (code >= 95 && code <= 99) return 'Thunderstorm';
  return 'Cloudy';
}

class ResultsScreen extends ConsumerStatefulWidget {
  final Map<String, dynamic> scan;
  const ResultsScreen({super.key, required this.scan});

  @override
  ConsumerState<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends State<ResultsScreen> {
  final FlutterTts _flutterTts = FlutterTts();

  @override
  void initState() {
    super.initState();
    _speakResult();
  }

  Future<void> _speakResult() async {
    final isSoil = widget.scan['isSoilAnalysis'] == true;
    final resultText = isSoil
        ? 'Soil type: ${widget.scan['soilType']}. Health: ${widget.scan['soilHealth']}'
        : 'Diagnosis: ${widget.scan['diseaseName']}. Treatment: ${widget.scan['treatment']}';
    await _flutterTts.setLanguage("en-US");
    await _flutterTts.speak(resultText);
  }

  @override
  void dispose() {
    _flutterTts.stop();
    super.dispose();
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final scan = widget.scan;
    final isSoil = scan['isSoilAnalysis'] == true;
    final aiSource = scan['aiSource'] ?? 'local';
    final baseUrl = ref.watch(serverBaseUrlProvider);

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          SliverAppBar(
            expandedHeight: 320,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(
              background: _buildImageWidget(scan, baseUrl),
            ),
            backgroundColor: AppColors.primary,
            leading: IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.pop(context),
            ),
            actions: [
              _buildAiBadge(aiSource),
            ],
          ),
          SliverToBoxAdapter(
            child: Transform.translate(
              offset: const Offset(0, -30),
              child: Container(
                padding: const EdgeInsets.all(24),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(32)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    _buildHeader(isSoil),
                    const SizedBox(height: 24),
                    if (scan['weather'] != null) _buildWeatherCard(scan['weather']),
                    const SizedBox(height: 20),
                    _buildDiagnosisCard(isSoil),
                    const SizedBox(height: 16),
                    if (scan['cause'] != null && scan['cause'].toString().isNotEmpty)
                      _buildInsightCard('Cause / Pathogen', scan['cause'], Icons.bug_report_outlined, Colors.deepOrange),
                    if (scan['pesticide'] != null && scan['pesticide'].toString().isNotEmpty)
                      _buildInsightCard('Recommended Pesticide', scan['pesticide'], Icons.grain, Colors.red),
                    if (scan['fertilizer'] != null && scan['fertilizer'].toString().isNotEmpty)
                      _buildInsightCard('Fertilizer', scan['fertilizer'], Icons.grass, Colors.green),
                    if (scan['prevention'] != null && scan['prevention'].toString().isNotEmpty)
                      _buildInsightCard('Prevention', scan['prevention'], Icons.health_and_safety, Colors.blue),
                    const SizedBox(height: 24),
                    _buildProductSection(scan),
                    const SizedBox(height: 32),
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildImageWidget(Map<String, dynamic> scan, String baseUrl) {
    final imageUrl = scan['imageUrl'] ?? '';
    if (imageUrl.startsWith('local://')) {
      return Container(
        color: AppColors.background,
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.image, size: 80, color: AppColors.textSecondary),
              SizedBox(height: 16),
              Text('Scan captured', textAlign: TextAlign.center, style: TextStyle(color: AppColors.textSecondary, fontSize: 16)),
            ],
          ),
        ),
      );
    } else if (imageUrl.startsWith('http')) {
      return CachedNetworkImage(
        imageUrl: imageUrl,
        fit: BoxFit.cover,
        placeholder: (context, url) => Container(color: AppColors.background, child: const Center(child: CircularProgressIndicator())),
        errorWidget: (context, url, error) => Container(
          color: AppColors.background,
          child: const Center(child: Icon(Icons.broken_image, size: 48, color: AppColors.textSecondary)),
        ),
      );
    } else {
      return Image.network(
        '$baseUrl$imageUrl',
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) => Container(
          color: AppColors.background,
          child: const Center(child: Icon(Icons.broken_image, size: 48, color: AppColors.textSecondary)),
        ),
        loadingBuilder: (context, child, loadingProgress) {
          if (loadingProgress == null) return child;
          return Container(
            color: AppColors.background,
            child: Center(child: CircularProgressIndicator(value: loadingProgress.expectedTotalBytes != null ? loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes! : null)),
          );
        },
      );
    }
  }

  Widget _buildAiBadge(String aiSource) {
    Color color;
    String label;
    switch (aiSource) {
      case 'gemini_vision':
        color = Colors.deepPurple;
        label = 'AI Vision';
        break;
      case 'on_device':
        color = Colors.teal;
        label = 'On-Device';
        break;
      default:
        color = Colors.blueGrey;
        label = 'Local';
    }
    return Padding(
      padding: const EdgeInsets.only(right: 16),
      child: Center(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
          decoration: BoxDecoration(color: color.withOpacity(0.9), borderRadius: BorderRadius.circular(20)),
          child: Text(label, style: const TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
        ),
      ),
    );
  }

  Widget _buildHeader(bool isSoil) {
    final scan = widget.scan;
    final c = scan['confidence'];
    final pct = c is num ? (c * 100).round() : 0;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          isSoil ? 'Soil Analysis' : 'Diagnosis',
          style: const TextStyle(color: AppColors.textSecondary, fontWeight: FontWeight.bold, letterSpacing: 1, fontSize: 12),
        ),
        const SizedBox(height: 6),
        Text(
          isSoil ? (scan['soilType'] ?? 'Unknown Soil') : (scan['diseaseName'] ?? 'Unknown'),
          style: const TextStyle(fontSize: 26, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
        ),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: AppColors.accent.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: AppColors.accent.withOpacity(0.3)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Icon(Icons.check_circle, color: AppColors.accent, size: 16),
              const SizedBox(width: 6),
              Text('$pct% confidence', style: const TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold, fontSize: 13)),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildWeatherCard(Map<String, dynamic>? weather) {
    if (weather == null) return const SizedBox.shrink();
    final temp = weather['temp']?.toString() ?? '--';
    final condition = weather['condition']?.toString() ?? '';
    final humidity = weather['humidity']?.toString() ?? '--';
    final wind = weather['windSpeed']?.toString() ?? '--';
    final icon = weather['icon'] as IconData? ?? Icons.cloud;

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [Colors.blue.shade400, Colors.lightBlue.shade200]),
        borderRadius: BorderRadius.circular(20),
        boxShadow: [BoxShadow(color: Colors.blue.shade200.withOpacity(0.4), blurRadius: 12, offset: const Offset(0, 6))],
      ),
      child: Row(
        children: [
          Icon(icon, color: Colors.white, size: 36),
          const SizedBox(width: 16),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('$temp°C, $condition', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 16)),
                const SizedBox(height: 4),
                Text('Humidity: $humidity%  •  Wind: ${wind}km/h', style: const TextStyle(color: Colors.white70, fontSize: 12)),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildDiagnosisCard(bool isSoil) {
    final scan = widget.scan;
    final severity = (scan['severity'] ?? 'Medium').toString().toLowerCase();
    Color severityColor;
    if (severity.contains('high')) severityColor = Colors.red;
    else if (severity.contains('medium')) severityColor = Colors.orange;
    else severityColor = Colors.green;

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.medical_services, color: AppColors.primary, size: 20),
              const SizedBox(width: 8),
              Text(isSoil ? 'Soil Health Assessment' : 'Disease Identification', style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: AppColors.textPrimary)),
            ],
          ),
          const SizedBox(height: 12),
          if (isSoil)
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoRow('Soil Type', scan['soilType']?.toString() ?? 'Unknown'),
                const SizedBox(height: 8),
                _buildInfoRow('Health', scan['soilHealth']?.toString() ?? 'Unknown'),
              ],
            )
          else
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildInfoRow('Plant', scan['plantName']?.toString() ?? 'Unknown'),
                const SizedBox(height: 8),
                _buildInfoRow('Problem', scan['diseaseName']?.toString() ?? 'Unknown'),
                const SizedBox(height: 8),
                Row(
                  children: [
                    SizedBox(
                      width: 80,
                      child: Text('Severity', style: TextStyle(color: Colors.grey[600], fontSize: 13)),
                    ),
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 4),
                      decoration: BoxDecoration(color: severityColor.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                      child: Text(severity.toUpperCase(), style: TextStyle(color: severityColor, fontWeight: FontWeight.bold, fontSize: 11)),
                    ),
                  ],
                ),
              ],
            ),
        ],
      ),
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        SizedBox(width: 80, child: Text(label, style: TextStyle(color: Colors.grey[600], fontSize: 13))),
        Expanded(child: Text(value, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500))),
      ],
    );
  }

  Widget _buildInsightCard(String title, String content, IconData icon, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: 12),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: color.withOpacity(0.05),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, color: color, size: 18),
              const SizedBox(width: 8),
              Text(title.toUpperCase(), style: const TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: AppColors.textSecondary, letterSpacing: 0.5)),
            ],
          ),
          const SizedBox(height: 8),
          Text(content, style: const TextStyle(fontSize: 14, height: 1.6, color: AppColors.textPrimary)),
        ],
      ),
    );
  }

  Widget _buildProductSection(Map<String, dynamic> scan) {
    final error = scan['productResearchError'];
    if (error != null) {
      return Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: Colors.amber.shade50,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: Colors.amber.shade200),
        ),
        child: Row(
          children: [
            const Icon(Icons.info_outline, color: Colors.amber, size: 24),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                'Product recommendations are unavailable. Check internet or AI settings.',
                style: TextStyle(color: Colors.amber.shade900, fontSize: 13, height: 1.5),
              ),
            ),
          ],
        ),
      );
    }

    final pr = scan['productResearch'];
    if (pr == null || pr is! Map) {
      return Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(color: Colors.grey.shade50, borderRadius: BorderRadius.circular(16)),
        child: const Center(
          child: Text('Finding best products for you...', style: TextStyle(color: AppColors.textSecondary)),
        ),
      );
    }

    final List suggestions = pr['suggestions'] ?? [];

    if (suggestions.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        if (pr['researchSummary'] != null)
          Padding(
            padding: const EdgeInsets.only(bottom: 16),
            child: Text(pr['researchSummary'], style: const TextStyle(color: AppColors.textSecondary, fontSize: 13, fontStyle: FontStyle.italic)),
          ),
        ...suggestions.map<Widget>((item) {
          final name = item['productName']?.toString() ?? 'Product';
          final type = item['productType']?.toString() ?? '';
          final ingredient = item['activeIngredient']?.toString() ?? '';
          final why = item['whyItFits']?.toString() ?? '';
          final tip = item['applicationTip']?.toString() ?? '';
          final safety = item['safetyNote']?.toString() ?? '';
          final buyUrl = item['purchaseUrl']?.toString();

          return Container(
            margin: const EdgeInsets.only(bottom: 16),
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(20),
              border: Border.all(color: Colors.grey.shade200),
              boxShadow: [BoxShadow(color: Colors.black.withOpacity(0.04), blurRadius: 8, offset: const Offset(0, 4))],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Text(name, style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w800, color: AppColors.textPrimary)),
                    ),
                    if (type.isNotEmpty)
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                        decoration: BoxDecoration(color: AppColors.accent.withOpacity(0.15), borderRadius: BorderRadius.circular(8)),
                        child: Text(type, style: const TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold, fontSize: 10)),
                      ),
                  ],
                ),
                if (ingredient.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.science, size: 14, color: AppColors.textSecondary),
                      const SizedBox(width: 4),
                      Expanded(child: Text(ingredient, style: const TextStyle(color: AppColors.textSecondary, fontSize: 12))),
                    ],
                  ),
                ],
                const SizedBox(height: 12),
                Text(why, style: const TextStyle(fontSize: 14, height: 1.5, color: AppColors.textPrimary)),
                if (tip.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.tips_and_updates, size: 14, color: AppColors.accent),
                      const SizedBox(width: 4),
                      Expanded(child: Text('Tip: $tip', style: const TextStyle(color: AppColors.accent, fontSize: 12))),
                    ],
                  ),
                ],
                if (safety.isNotEmpty) ...[
                  const SizedBox(height: 8),
                  Row(
                    children: [
                      const Icon(Icons.warning_amber, size: 14, color: Colors.orange),
                      const SizedBox(width: 4),
                      Expanded(child: Text('Safety: $safety', style: const TextStyle(color: Colors.orange, fontSize: 12))),
                    ],
                  ),
                ],
                if (buyUrl != null && buyUrl.isNotEmpty) ...[
                  const SizedBox(height: 16),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton.icon(
                      onPressed: () => launchUrl(Uri.parse(buyUrl), mode: LaunchMode.externalApplication),
                      icon: const Icon(Icons.shopping_cart, size: 16),
                      label: const Text('BUY PRODUCT', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1)),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: AppColors.accent,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 14),
                        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                      ),
                    ),
                  ),
                ],
              ],
            ),
          );
        }).toList(),
      ],
    );
  }
}
