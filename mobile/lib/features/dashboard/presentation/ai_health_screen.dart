import 'package:flutter/material.dart';
import '../../../core/theme/app_theme.dart';

class AIHealthScreen extends StatelessWidget {
  const AIHealthScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Health Dashboard'),
        backgroundColor: AppColors.primary,
      ),
      body: const Center(
        child: Text('AI Health Monitoring Coming Soon'),
      ),
    );
  }
}