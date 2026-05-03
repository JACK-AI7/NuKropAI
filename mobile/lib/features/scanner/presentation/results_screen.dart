import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../core/theme/app_theme.dart';
import '../../../core/config/constants.dart';
import 'package:flutter_tts/flutter_tts.dart';
import 'package:url_launcher/url_launcher.dart';
import 'package:cached_network_image/cached_network_image.dart';

// Helper to get weather icon from code (all constants for tree-shaking)
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

class ResultsScreen extends StatefulWidget {
  final Map<String, dynamic> scan;
  const ResultsScreen({super.key, required this.scan});

  @override
  State<ResultsScreen> createState() => _ResultsScreenState();
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
  Widget build(BuildContext context) {
    final scan = widget.scan;
    final isSoil = scan['isSoilAnalysis'] == true;
    final String baseUrl = AppConstants.baseUrl.replaceAll('/api', '');
    final aiSource = scan['aiSource'] ?? 'backend';
    final aiError = scan['_error'] == true ? scan['message'] : null;
    final aiWarning = scan['_aiWarning'] == true ? scan['_aiWarningMessage']?.toString() : null;

    // Image widget
    Widget imageWidget;
    final imageUrl = scan['imageUrl'] ?? '';
    if (imageUrl.startsWith('local://')) {
      imageWidget = Container(
        color: AppColors.background,
        child: const Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(Icons.image, size: 64, color: AppColors.textSecondary),
              SizedBox(height: 16),
              Text('Scan captured locally', textAlign: TextAlign.center, style: TextStyle(color: AppColors.textSecondary)),
            ],
          ),
        ),
      );
    } else if (imageUrl.startsWith('http')) {
      imageWidget = Image.network(
        imageUrl,
        fit: BoxFit.cover,
        errorBuilder: (context, error, stackTrace) => Container(
          color: AppColors.background,
          child: const Center(child: Icon(Icons.broken_image, size: 48, color: AppColors.textSecondary)),
        ),
        loadingBuilder: (context, child, loadingProgress) {
          if (loadingProgress == null) return child;
          return Container(
            color: AppColors.background,
            child: Center(
              child: CircularProgressIndicator(
                value: loadingProgress.expectedTotalBytes != null
                    ? loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes!
                    : null,
              ),
            ),
          );
        },
      );
    } else {
      imageWidget = Image.network(
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
            child: Center(
              child: CircularProgressIndicator(
                value: loadingProgress.expectedTotalBytes != null
                    ? loadingProgress.cumulativeBytesLoaded / loadingProgress.expectedTotalBytes!
                    : null,
              ),
            ),
          );
        },
      );
    }

    return Scaffold(
      backgroundColor: Colors.white,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          SliverAppBar(
            expandedHeight: 400,
            pinned: true,
            flexibleSpace: FlexibleSpaceBar(background: imageWidget),
            backgroundColor: AppColors.primary,
            leading: IconButton(
              icon: const Icon(Icons.arrow_back, color: Colors.white),
              onPressed: () => Navigator.pop(context),
            ),
            actions: [
              if (aiSource == 'mistral')
                Padding(
                  padding: const EdgeInsets.only(right: 16),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(color: Colors.deepOrange.withOpacity(0.95), borderRadius: BorderRadius.circular(20)),
                      child: const Text('Mistral', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                    ),
                  ),
                )
              else if (aiSource == 'ollama')
                Padding(
                  padding: const EdgeInsets.only(right: 16),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(color: Colors.teal.withOpacity(0.9), borderRadius: BorderRadius.circular(20)),
                      child: const Text('Ollama', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                    ),
                  ),
                )
              else if (aiSource == 'database')
                Padding(
                  padding: const EdgeInsets.only(right: 16),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                      decoration: BoxDecoration(color: Colors.deepPurple.withOpacity(0.85), borderRadius: BorderRadius.circular(20)),
                      child: const Text('Database', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.bold)),
                    ),
                  ),
                ),
            ],
          ),
          SliverToBoxAdapter(
            child: Transform.translate(
              offset: const Offset(0, -30),
              child: Container(
                padding: const EdgeInsets.all(32),
                decoration: const BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.vertical(top: Radius.circular(40)),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    // AI Error Card (if any)
                    if (aiError != null)
                      FadeInDown(
                        child: Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.red.shade50,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: Colors.red.shade200),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.error_outline, color: Colors.red, size: 24),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Text(
                                      'AI Analysis Error',
                                      style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold, fontSize: 14),
                                    ),
                                    const SizedBox(height: 4),
                                    Text(
                                      aiError,
                                      style: const TextStyle(color: Colors.red, fontSize: 13, height: 1.4),
                                    ),
                                  ],
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    if (aiError != null) const SizedBox(height: 20),
                    if (aiWarning != null)
                      FadeInDown(
                        child: Container(
                          padding: const EdgeInsets.all(16),
                          decoration: BoxDecoration(
                            color: Colors.amber.shade50,
                            borderRadius: BorderRadius.circular(16),
                            border: Border.all(color: Colors.amber.shade200),
                          ),
                          child: Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Icon(Icons.info_outline, color: Colors.amber.shade900, size: 24),
                              const SizedBox(width: 12),
                              Expanded(
                                child: Text(
                                  aiWarning,
                                  style: TextStyle(color: Colors.amber.shade900, fontSize: 13, height: 1.4),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    if (aiWarning != null) const SizedBox(height: 20),
                    _buildHeader(context, isSoil),
                    const SizedBox(height: 32),
                    _buildSeveritySection(context, isSoil),
                    const SizedBox(height: 28),
                    if (scan['cause'] != null && scan['cause'].toString().isNotEmpty) ...[
                      _buildInsightCard(
                        context,
                        'CAUSE / PATHOGEN',
                        scan['cause'].toString(),
                        Icons.bug_report_outlined,
                        Colors.deepOrange,
                      ),
                      const SizedBox(height: 18),
                    ],
                    _buildInsightCard(
                      context,
                      isSoil ? 'SOIL HEALTH' : 'TREATMENT',
                      isSoil ? (scan['soilHealth'] ?? 'N/A') : (scan['treatment'] ?? 'N/A'),
                      isSoil ? Icons.health_and_safety : Icons.medical_services,
                      Colors.blue,
                    ),
                    const SizedBox(height: 18),
                    _buildInsightCard(
                      context,
                      isSoil ? 'RECOMMENDATIONS' : 'FERTILIZER',
                      isSoil ? (scan['nutrients'] ?? 'N/A') : (scan['fertilizer'] ?? 'N/A'),
                      isSoil ? Icons.tips_and_updates : Icons.grass,
                      Colors.green,
                    ),
                    if (scan['pesticide'] != null && scan['pesticide'].toString().isNotEmpty) ...[
                      const SizedBox(height: 18),
                      _buildInsightCard(
                        context,
                        'PESTICIDE',
                        scan['pesticide'],
                        Icons.grain,
                        Colors.orange,
                      ),
                    ],
                    const SizedBox(height: 24),
                    _buildAiProductResearchSection(context, scan),
                    const SizedBox(height: 24),
                    _buildNPKSection(context),
                    const SizedBox(height: 16),
                    if (scan['weather'] != null) ...[
                      _buildWeatherCard(context, scan['weather']),
                      const SizedBox(height: 24),
                    ],
                  ],
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeader(BuildContext context, bool isSoil) {
    final scan = widget.scan;
    final c = scan['confidence'];
    final pct = c is num ? (c * 100).round() : 0;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          isSoil ? 'Soil Analysis' : 'Diagnosis',
          style: const TextStyle(color: AppColors.textSecondary, fontWeight: FontWeight.bold, letterSpacing: 1),
        ),
        const SizedBox(height: 8),
        Text(
          isSoil ? scan['soilType'] : scan['diseaseName'],
          style: Theme.of(context).textTheme.headlineMedium,
        ),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: AppColors.accent.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Text(
            '$pct% model confidence',
            style: const TextStyle(color: AppColors.accent, fontWeight: FontWeight.bold),
          ),
        ),
      ],
    );
  }

  Widget _buildSeveritySection(BuildContext context, bool isSoil) {
    final scan = widget.scan;
    if (isSoil) return const SizedBox.shrink();
    return Row(
      children: [
        _severityDot(scan['severity']?.toString() ?? 'Low'),
        const SizedBox(width: 12),
        Text(
          'Severity: ${scan['severity'] ?? 'Unknown'}',
          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
        ),
      ],
    );
  }

  Widget _buildAiProductResearchSection(BuildContext context, Map<String, dynamic> scan) {
    final err = scan['productResearchError']?.toString();
    final source = scan['productResearchSource']?.toString();
    final raw = scan['productResearch'];
    Map<String, dynamic>? pr;
    if (raw is Map) {
      pr = Map<String, dynamic>.from(raw as Map);
    }

    return FadeInUp(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
          const Text(
            'AI PRODUCT RESEARCH (MISTRAL)',
            style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1, color: AppColors.textSecondary, fontSize: 12),
          ),
              if (source != null && source.isNotEmpty) ...[
                const SizedBox(width: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                  decoration: BoxDecoration(
                    color: AppColors.offWhite,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Text(
                    source,
                    style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppColors.textDark),
                  ),
                ),
              ],
            ],
          ),
          const SizedBox(height: 8),
          Text(
            'After the scan identifies the issue, Mistral (cloud) or your local Ollama model researches suitable products for your GPS region. Always confirm with dealers, extension staff, and label directions.',
            style: TextStyle(fontSize: 12, height: 1.4, color: Colors.grey.shade600),
          ),
          const SizedBox(height: 12),
          if (err != null && err.isNotEmpty)
            Text(
              'Product research unavailable: $err',
              style: TextStyle(fontSize: 13, height: 1.5, color: Colors.orange.shade900),
            )
          else if (pr == null)
            const Text(
              'No product research in this response.',
              style: TextStyle(fontSize: 13, color: AppColors.textSecondary),
            )
          else ...[
            if (pr['researchSummary'] != null && pr['researchSummary'].toString().isNotEmpty)
              Padding(
                padding: const EdgeInsets.only(bottom: 16),
                child: Text(
                  pr['researchSummary'].toString(),
                  style: const TextStyle(fontSize: 14, height: 1.55, fontWeight: FontWeight.w500),
                ),
              ),
            if (pr['suggestions'] is! List || (pr['suggestions'] as List).isEmpty)
              const Text('No suggestions returned.', style: TextStyle(fontSize: 13))
            else
              ...(pr['suggestions'] as List).map<Widget>((e) {
                final m = Map<String, dynamic>.from(e as Map);
                final buyUrl = m['purchaseUrl']?.toString();
                final prodImg = m['imageUrl']?.toString();

                return Container(
                  margin: const EdgeInsets.only(bottom: 20),
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(24),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withOpacity(0.04),
                        blurRadius: 20,
                        offset: const Offset(0, 10),
                      ),
                    ],
                  ),
                  child: ClipRRect(
                    borderRadius: BorderRadius.circular(24),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        if (prodImg != null && prodImg.isNotEmpty)
                          SizedBox(
                            height: 180,
                            width: double.infinity,
                            child: CachedNetworkImage(
                              imageUrl: prodImg,
                              fit: BoxFit.cover,
                              placeholder: (context, url) => Container(
                                color: AppColors.background,
                                child: const Center(child: CircularProgressIndicator(strokeWidth: 2)),
                              ),
                              errorWidget: (context, url, error) => Container(
                                color: AppColors.background,
                                child: const Icon(Icons.inventory_2_outlined, size: 48, color: AppColors.textSecondary),
                              ),
                            ),
                          ),
                        Padding(
                          padding: const EdgeInsets.all(20),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Expanded(
                                    child: Text(
                                      m['productName']?.toString() ?? 'Product',
                                      style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18, letterSpacing: -0.5),
                                    ),
                                  ),
                                  if (m['productType'] != null)
                                    Container(
                                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                                      decoration: BoxDecoration(
                                        color: AppColors.primary.withOpacity(0.1),
                                        borderRadius: BorderRadius.circular(8),
                                      ),
                                      child: Text(
                                        m['productType'].toString(),
                                        style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: AppColors.primary),
                                      ),
                                    ),
                                ],
                              ),
                              if (m['activeIngredient'] != null && m['activeIngredient'].toString().isNotEmpty)
                                Padding(
                                  padding: const EdgeInsets.only(top: 8),
                                  child: Text(
                                    'Active: ${m['activeIngredient']}',
                                    style: TextStyle(fontSize: 13, color: Colors.grey.shade700, fontWeight: FontWeight.w500),
                                  ),
                                ),
                              const SizedBox(height: 12),
                              Text(
                                m['whyItFits']?.toString() ?? '',
                                style: const TextStyle(fontSize: 14, height: 1.5, color: AppColors.textDark),
                              ),
                              const SizedBox(height: 16),
                              if (m['applicationTip'] != null)
                                _buildMiniInfo(Icons.info_outline, 'Tip: ${m['applicationTip']}', Colors.blueGrey),
                              if (m['regionalAvailability'] != null)
                                _buildMiniInfo(Icons.location_on_outlined, 'Availability: ${m['regionalAvailability']}', Colors.teal),
                              
                              if (buyUrl != null && buyUrl.isNotEmpty) ...[
                                const SizedBox(height: 20),
                                SizedBox(
                                  width: double.infinity,
                                  child: ElevatedButton.icon(
                                    onPressed: () async {
                                      final uri = Uri.parse(buyUrl);
                                      if (await canLaunchUrl(uri)) {
                                        await launchUrl(uri, mode: LaunchMode.externalApplication);
                                      }
                                    },
                                    icon: const Icon(Icons.shopping_cart_outlined, size: 18, color: Colors.white),
                                    label: const Text('VIEW PRODUCT', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1, color: Colors.white)),
                                    style: ElevatedButton.styleFrom(
                                      backgroundColor: AppColors.primary,
                                      foregroundColor: Colors.white,
                                      padding: const EdgeInsets.symmetric(vertical: 16),
                                      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
                                      elevation: 0,
                                    ),
                                  ),
                                ),
                              ],
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }),
          ],
        ],
      ),
    );
  }

  Widget _buildMiniInfo(IconData icon, String text, Color color) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 6),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 14, color: color),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              text,
              style: TextStyle(fontSize: 12, color: color.withOpacity(0.9), height: 1.4),
            ),
          ),
        ],
      ),
    );
  }

  Widget _severityDot(String severity) {
    Color color = Colors.green;
    if (severity.toLowerCase() == 'medium') color = Colors.orange;
    if (severity.toLowerCase() == 'high') color = Colors.red;
    return Container(
      width: 12,
      height: 12,
      decoration: BoxDecoration(color: color, shape: BoxShape.circle),
    );
  }

  Widget _buildInsightCard(BuildContext context, String title, String value, IconData icon, Color color) {
    return FadeInUp(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: AppColors.background,
          borderRadius: BorderRadius.circular(24),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 20),
                const SizedBox(width: 12),
                Text(title, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 13, letterSpacing: 0.5)),
              ],
            ),
            const SizedBox(height: 12),
            Text(
              value,
              style: const TextStyle(fontSize: 15, height: 1.6, fontWeight: FontWeight.w500),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNPKSection(BuildContext context) {
    final scan = widget.scan;
    final npkData = scan['npk'];
    final List<double> npkValues = [];
    if (npkData is Map) {
      npkValues.add((npkData['N'] ?? 0).toDouble());
      npkValues.add((npkData['P'] ?? 0).toDouble());
      npkValues.add((npkData['K'] ?? 0).toDouble());
    } else if (npkData is List) {
      npkValues.addAll(npkData.map((e) => (e as num).toDouble()));
    } else {
      npkValues.addAll([0, 0, 0]);
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('NPK LEVELS', style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1, color: AppColors.textSecondary, fontSize: 12)),
        const SizedBox(height: 20),
        SizedBox(
          height: 180,
          child: BarChart(
            BarChartData(
              alignment: BarChartAlignment.spaceAround,
              maxY: 100,
              barTouchData: BarTouchData(enabled: false),
              titlesData: FlTitlesData(
                show: true,
                bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                    showTitles: true,
                    getTitlesWidget: (value, meta) {
                      const titles = ['N', 'P', 'K'];
                      return Text(titles[value.toInt()], style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13));
                    },
                  ),
                ),
                leftTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                topTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
                rightTitles: const AxisTitles(sideTitles: SideTitles(showTitles: false)),
              ),
              gridData: const FlGridData(show: false),
              borderData: FlBorderData(show: false),
              barGroups: [
                _buildBarGroup(0, npkValues.length > 0 ? npkValues[0] : 0, Colors.blue),
                _buildBarGroup(1, npkValues.length > 1 ? npkValues[1] : 0, Colors.green),
                _buildBarGroup(2, npkValues.length > 2 ? npkValues[2] : 0, Colors.orange),
              ],
            ),
          ),
        ),
      ],
    );
  }

  BarChartGroupData _buildBarGroup(int x, double y, Color color) {
    return BarChartGroupData(
      x: x,
      barRods: [
        BarChartRodData(
          toY: y,
          color: color,
          width: 40,
          borderRadius: BorderRadius.circular(10),
          backDrawRodData: BackgroundBarChartRodData(show: true, toY: 100, color: AppColors.background),
        ),
      ],
    );
  }

  Widget _buildWeatherCard(BuildContext context, dynamic weatherData) {
    Map<String, dynamic> weather;
    if (weatherData is String) {
      try {
        weather = jsonDecode(weatherData);
      } catch (e) {
        weather = {'temp': '--', 'condition': 'N/A', 'humidity': '--', 'windSpeed': '--', 'weatherCode': null};
      }
    } else {
      weather = weatherData as Map<String, dynamic>;
    }

    final tempRaw = weather['temp'];
    final temp = tempRaw is num ? tempRaw.toStringAsFixed(0) : '--';
    var condition = weather['condition']?.toString() ?? '';
    if (condition.isEmpty && weather['weatherCode'] != null) {
      final code = weather['weatherCode'];
      condition = getWeatherCondition(code is num ? code.toInt() : int.tryParse(code.toString()));
    }
    final humidity = weather['humidity']?.toString() ?? '--';
    final windSpeed = weather['windSpeed']?.toString() ?? '--';
    final weatherCode = weather['weatherCode'];
    final iconData = getWeatherIcon(weatherCode);

    return FadeInUp(
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          gradient: LinearGradient(
            colors: [Colors.blue.shade400, Colors.blue.shade700],
            begin: Alignment.topLeft,
            end: Alignment.bottomRight,
          ),
          borderRadius: BorderRadius.circular(24),
        ),
        child: Row(
          children: [
            Icon(iconData, color: Colors.white, size: 40),
            const SizedBox(width: 20),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Text('$temp°C', style: const TextStyle(color: Colors.white, fontSize: 32, fontWeight: FontWeight.bold)),
                      const SizedBox(width: 8),
                      Flexible(
                        child: Text(
                          condition,
                          style: const TextStyle(color: Colors.white70, fontSize: 14, fontWeight: FontWeight.w500),
                          overflow: TextOverflow.ellipsis,
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 4),
                  Text('Humidity: $humidity%  •  Wind: ${windSpeed}km/h', style: const TextStyle(color: Colors.white70, fontSize: 12)),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
