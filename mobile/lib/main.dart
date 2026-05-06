import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/l10n/app_localizations.dart';
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
  
  try {
    await Firebase.initializeApp(
      options: DefaultFirebaseOptions.currentPlatform,
    );
    debugPrint("Firebase Initialized Successfully");
    
    await RemoteConfigService.initialize();
    debugPrint("Remote Config Initialized Successfully");
  } catch (e) {
    debugPrint("Firebase/Remote Config Initialization Error: $e");
  }

  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends ConsumerWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final authState = ref.watch(authProvider);
    final currentLocale = ref.watch(localeProvider);
    
    // Initialize server URL on first build
    ref.watch(serverUrlInitializationProvider);

    return MaterialApp(
      title: 'NuKropAI',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.hybridTheme,
      locale: currentLocale,
      localizationsDelegates: const [
        AppLocalizations.delegate,
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [
        Locale('en'),
        Locale('hi'),
        Locale('te'),
        Locale('ta'),
        Locale('kn'),
        Locale('mr'),
        Locale('bn'),
      ],
      home: authState.isLoading
          ? const Scaffold(body: Center(child: CircularProgressIndicator()))
          : authState.isAuthenticated
              ? const DashboardScreen()
              : const LoginScreen(),
    );
  }
}

/// FutureProvider to load and set the server URL on app startup
final serverUrlInitializationProvider = FutureProvider<void>((ref) async {
  final config = ref.read(serverConfigProvider);
  final savedUrl = await config.getServerUrl();
  ref.read(serverUrlProvider.notifier).state = savedUrl;
});
