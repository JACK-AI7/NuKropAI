import 'package:flutter/material.dart';
import 'package:animate_do/animate_do.dart';
import '../../../core/theme/app_theme.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    // In real app, the main.dart handles routing based on auth
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            FadeInDown(
              child: const Icon(Icons.eco_rounded, size: 100, color: AppColors.primary),
            ),
            const SizedBox(height: 24),
            FadeInUp(
              child: Text(
                'SMART FARM',
                style: Theme.of(context).textTheme.headlineLarge?.copyWith(
                  letterSpacing: 5,
                  color: AppColors.primary,
                ),
              ),
            ),
            const SizedBox(height: 8),
            FadeInUp(
              delay: const Duration(milliseconds: 200),
              child: const Text(
                'AI POWERED AGRICULTURE',
                style: TextStyle(letterSpacing: 2, color: Colors.white54),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
