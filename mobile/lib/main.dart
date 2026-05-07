import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/l10n/app_localizations_delegate.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/presentation/login_screen.dart';
import 'features/dashboard/presentation/dashboard_screen.dart';
import 'features/auth/data/auth_repository.dart';
import 'core/api/server_config.dart';

import 'package:flutter_localizations/flutter_localizations.dart';
import 'core/l10n/locale_provider.dart';

import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';
import 'core/config/remote_config_service.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Custom Error Widget to debug grey screens
  ErrorWidget.builder = (FlutterErrorDetails details) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      body: Container(
        padding: const EdgeInsets.all(32),
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Icon(Icons.bug_report, color: Colors.redAccent, size: 80),
              const SizedBox(height: 24),
              const Text(
                "SYSTEM ERROR",
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.w900, fontSize: 24, letterSpacing: 2),
              ),
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white.withOpacity(0.05),
                  borderRadius: BorderRadius.circular(16),
                  border: Border.all(color: Colors.white10),
                ),
                child: Text(
                  details.exception.toString(),
                  style: const TextStyle(color: Colors.white70, fontSize: 13, fontFamily: 'monospace'),
                  textAlign: TextAlign.center,
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                "Please screenshot this and send to support.",
                style: TextStyle(color: Colors.white38, fontSize: 12),
              ),
            ],
          ),
        ),
      ),
    );
  };

  try {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
  } catch (e) {
    debugPrint("Firebase Init Error");
  }

  try {
    await RemoteConfigService.initialize();
  } catch (e) {
    debugPrint("Remote Config Init Error");
  }

  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    final currentLocale = ref.watch(localeProvider);

    return MaterialApp(
      title: 'NuKropAI',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.hybridTheme,
      locale: currentLocale,
      localizationsDelegates: const [
        AppLocalizationsDelegate(),
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en'),
        Locale('hi'),
        Locale('te'),
      ],
      home: authState.isLoading
          ? const Scaffold(
              backgroundColor: Color(0xFF0F172A),
              body: Center(
                child: CircularProgressIndicator(color: Color(0xFF4CAF50)),
              ),
            )
          : authState.isAuthenticated
              ? const DashboardScreen()
              : const LoginScreen(),
    );
  }
}
