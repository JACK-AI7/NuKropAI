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
import '../../chat/presentation/chat_screen.dart';

class ResultsScreen extends ConsumerStatefulWidget {
  final Map<String, dynamic> scan;
  const ResultsScreen({super.key, required this.scan});

  @override
  ConsumerState<ResultsScreen> createState() => _ResultsScreenState();
}

class _ResultsScreenState extends ConsumerState<ResultsScreen> {
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
    final aiSource = scan['aiSource'] ?? 'backend';
    final baseUrl = ref.watch(serverBaseUrlProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // Background Gradient
          Positioned.fill(
            child: Container(
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [Color(0xFF0F172A), Color(0xFF1E293B)],
                ),
              ),
            ),
          ),

          CustomScrollView(
            physics: const BouncingScrollPhysics(),
            slivers: [
              SliverAppBar(
                expandedHeight: 300,
                pinned: true,
                backgroundColor: Colors.transparent,
                flexibleSpace: FlexibleSpaceBar(
                  background: Hero(
                    tag: scan['imageUrl'] ?? 'scan_image',
                    child: _buildImage(scan, baseUrl),
                  ),
                ),
                leading: _buildGlassActionIcon(Icons.arrow_back_ios_new_rounded, () => Navigator.pop(context)),
              ),
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      _buildHeaderSection(scan, isSoil, aiSource),
                      const SizedBox(height: 32),
                      _buildDiagnosticStats(scan),
                      const SizedBox(height: 32),
                      if (!isSoil) _buildGlassPestCard(scan),
                      if (!isSoil && scan['pestDetections'] != null) const SizedBox(height: 32),
                      _buildSectionTitle('ACTIONABLE INSIGHTS'),
                      const SizedBox(height: 16),
                      _buildGlassInsightList(scan, isSoil),
                      const SizedBox(height: 32),
                      _buildSectionTitle('BUYING OPTIONS & PRODUCTS'),
                      const SizedBox(height: 16),
                      _buildGlassProductResearch(scan),
                      const SizedBox(height: 32),
                      _buildSectionTitle('NPK PROFILE'),
                      const SizedBox(height: 16),
                      _buildGlassNPKCard(scan),
                      const SizedBox(height: 100),
                    ],
                  ),
                ),
              ),
            ],
          ),
          
          // Fixed Chat FAB
          Positioned(
            bottom: 30,
            right: 24,
            left: 24,
            child: _buildGlassChatCallout(scan),
          ),
        ],
      ),
    );
  }

  Widget _buildGlassActionIcon(IconData icon, VoidCallback onTap) {
    return Container(
      margin: const EdgeInsets.all(8),
      decoration: AppColors.glassDecoration(radius: 12),
      child: IconButton(
        icon: Icon(icon, color: Colors.white, size: 20),
        onPressed: onTap,
      ),
    );
  }

  Widget _buildImage(Map<String, dynamic> scan, String baseUrl) {
    final url = scan['imageUrl'] ?? '';
    if (url.startsWith('local://')) {
      return Container(color: Colors.black26, child: const Icon(Icons.image, size: 64, color: Colors.white24));
    }
    final fullUrl = url.startsWith('http') ? url : '$baseUrl$url';
    return CachedNetworkImage(
      imageUrl: fullUrl,
      fit: BoxFit.cover,
      placeholder: (context, url) => Container(color: Colors.black26),
      errorWidget: (context, url, error) => const Icon(Icons.broken_image, color: Colors.white24),
    );
  }

  Widget _buildHeaderSection(Map<String, dynamic> scan, bool isSoil, String aiSource) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Text(
              aiSource.toUpperCase(),
              style: const TextStyle(color: AppColors.accent, fontWeight: FontWeight.w900, fontSize: 10, letterSpacing: 2),
            ),
            const Spacer(),
            Icon(isSoil ? Icons.terrain_rounded : Icons.eco_rounded, color: Colors.white38, size: 16),
          ],
        ),
        const SizedBox(height: 8),
        Text(
          isSoil ? (scan['soilType'] ?? 'Unknown Soil') : (scan['diseaseName'] ?? 'Healthy'),
          style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold, letterSpacing: -1),
        ),
      ],
    );
  }

  Widget _buildDiagnosticStats(Map<String, dynamic> scan) {
    final conf = (scan['confidence'] is num) ? (scan['confidence'] as num) * 100 : 0;
    final severity = scan['severity']?.toString() ?? 'Medium';
    
    return Row(
      children: [
        _statCard('Confidence', '${conf.round()}%', AppColors.accent),
        const SizedBox(width: 16),
        _statCard('Severity', severity.toUpperCase(), _getSeverityColor(severity)),
      ],
    );
  }

  Widget _statCard(String label, String value, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: AppColors.glassDecoration(radius: 24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(color: Colors.white38, fontSize: 10, fontWeight: FontWeight.bold, letterSpacing: 1)),
            const SizedBox(height: 4),
            Text(value, style: TextStyle(color: color, fontSize: 20, fontWeight: FontWeight.w900)),
          ],
        ),
      ),
    );
  }

  Color _getSeverityColor(String severity) {
    severity = severity.toLowerCase();
    if (severity.contains('high')) return Colors.redAccent;
    if (severity.contains('low')) return Colors.greenAccent;
    return Colors.orangeAccent;
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: const TextStyle(color: Colors.white38, fontWeight: FontWeight.w900, fontSize: 11, letterSpacing: 2),
    );
  }

  Widget _buildGlassInsightList(Map<String, dynamic> scan, bool isSoil) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 32),
      child: Column(
        children: [
          _insightItem(isSoil ? Icons.health_and_safety : Icons.healing, isSoil ? 'Soil Health' : 'Treatment', isSoil ? scan['soilHealth'] : scan['treatment'], AppColors.accent),
          const Divider(height: 32, color: Colors.white10),
          _insightItem(isSoil ? Icons.eco : Icons.science, isSoil ? 'Nutrients' : 'Pesticide', isSoil ? scan['nutrients'] : (scan['pesticide'] ?? scan['fertilizer']), Colors.blueAccent),
          if (isSoil && scan['suitableCrops'] != null) ...[
            const Divider(height: 32, color: Colors.white10),
            _insightItem(Icons.agriculture, 'Best Crops', scan['suitableCrops'], Colors.orangeAccent),
          ],
        ],
      ),
    );
  }

  Widget _insightItem(IconData icon, String label, dynamic value, Color color) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(10),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(12)),
          child: Icon(icon, color: color, size: 20),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(label, style: const TextStyle(color: Colors.white38, fontSize: 10, fontWeight: FontWeight.bold)),
              const SizedBox(height: 2),
              Text(value?.toString() ?? 'N/A', style: const TextStyle(color: Colors.white, fontSize: 14, fontWeight: FontWeight.w500, height: 1.4)),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildGlassPestCard(Map<String, dynamic> scan) {
    final pestsStr = scan['pestDetections'];
    if (pestsStr == null) return const SizedBox.shrink();
    List<dynamic> pests = [];
    try { pests = jsonDecode(pestsStr as String); } catch (_) {}
    if (pests.isEmpty) return const SizedBox.shrink();

    return Container(
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 32),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.bug_report_rounded, color: Colors.purpleAccent, size: 20),
              SizedBox(width: 12),
              Text('PEST DETECTIONS', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 14)),
            ],
          ),
          const SizedBox(height: 16),
          ...pests.map((p) => Padding(
            padding: const EdgeInsets.only(bottom: 12),
            child: Row(
              children: [
                Text(p['species']?.toString() ?? 'Unknown', style: const TextStyle(color: Colors.white, fontSize: 15)),
                const Spacer(),
                Text('${((p['confidence'] ?? 0) * 100).round()}%', style: const TextStyle(color: Colors.purpleAccent, fontWeight: FontWeight.bold)),
              ],
            ),
          )),
        ],
      ),
    );
  }

  Widget _buildGlassProductResearch(Map<String, dynamic> scan) {
    final pr = scan['productResearch'];
    if (pr == null || pr is! Map) return const Center(child: Text('No buying options found.', style: TextStyle(color: Colors.white38)));
    
    final List suggestions = pr['suggestions'] ?? [];
    
    return Column(
      children: suggestions.map<Widget>((m) {
        final buyUrl = m['purchaseUrl']?.toString();
        return Container(
          margin: const EdgeInsets.only(bottom: 16),
          padding: const EdgeInsets.all(20),
          decoration: AppColors.glassDecoration(radius: 24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Expanded(child: Text(m['productName']?.toString() ?? 'Product', style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18))),
                  if (m['productType'] != null)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                      decoration: BoxDecoration(color: AppColors.accent.withOpacity(0.2), borderRadius: BorderRadius.circular(8)),
                      child: Text(m['productType'].toString(), style: const TextStyle(color: AppColors.accent, fontSize: 10, fontWeight: FontWeight.bold)),
                    ),
                ],
              ),
              const SizedBox(height: 8),
              Text('Active: ${m['activeIngredient'] ?? 'N/A'}', style: const TextStyle(color: Colors.white60, fontSize: 12, fontWeight: FontWeight.bold)),
              const SizedBox(height: 12),
              Text(m['whyItFits']?.toString() ?? '', style: const TextStyle(color: Colors.white70, fontSize: 13, height: 1.5)),
              if (buyUrl != null && buyUrl.isNotEmpty) ...[
                const SizedBox(height: 20),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton.icon(
                    onPressed: () => launchUrl(Uri.parse(buyUrl), mode: LaunchMode.externalApplication),
                    icon: const Icon(Icons.shopping_bag_outlined, size: 18),
                    label: const Text('BUY NOW', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1)),
                    style: ElevatedButton.styleFrom(backgroundColor: AppColors.accent, shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16))),
                  ),
                ),
              ],
            ],
          ),
        );
      }).toList(),
    );
  }

  Widget _buildGlassNPKCard(Map<String, dynamic> scan) {
    final npk = scan['npk'] ?? [0, 0, 0];
    final List<double> vals = (npk as List).map((e) => (e as num).toDouble()).toList();

    return Container(
      height: 200,
      padding: const EdgeInsets.all(24),
      decoration: AppColors.glassDecoration(radius: 32),
      child: BarChart(
        BarChartData(
          alignment: BarChartAlignment.spaceAround,
          maxY: 100,
          barTouchData: BarTouchData(enabled: false),
          titlesData: FlTitlesData(
            bottomTitles: AxisTitles(sideTitles: SideTitles(showTitles: true, getTitlesWidget: (v, m) => Text(['N', 'P', 'K'][v.toInt()], style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)))),
            leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
            rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
          ),
          gridData: const FlGridData(show: false),
          borderData: FlBorderData(show: false),
          barGroups: List.generate(3, (i) => BarChartGroupData(x: i, barRods: [BarChartRodData(toY: vals[i], color: [Colors.blue, Colors.green, Colors.orange][i], width: 30, borderRadius: BorderRadius.circular(8))])),
        ),
      ),
    );
  }

  Widget _buildGlassChatCallout(Map<String, dynamic> scan) {
    return GestureDetector(
      onTap: () {
        final diagnosis = scan['isSoilAnalysis'] == true ? scan['soilType'] : scan['diseaseName'];
        Navigator.push(context, MaterialPageRoute(builder: (_) => ChatScreen(initialMessage: "Tell me more about $diagnosis.")));
      },
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: AppColors.glassDecoration(radius: 32, highlight: true),
        child: Row(
          children: [
            const CircleAvatar(backgroundColor: AppColors.accent, child: Icon(Icons.auto_awesome, color: Colors.white, size: 20)),
            const SizedBox(width: 16),
            const Expanded(child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [Text('Discuss with AI', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)), Text('Get deeper insights', style: TextStyle(color: Colors.white38, fontSize: 11))])),
            const Icon(Icons.arrow_forward_ios_rounded, color: Colors.white24, size: 16),
          ],
        ),
      ),
    );
  }
}
