import 'package:flutter/material.dart';

class AppLocalizations {
  final Locale locale;
  AppLocalizations(this.locale);

  static AppLocalizations? of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations);
  }

  static AppLocalizations get instance => AppLocalizations(const Locale('en'));

  static const Map<String, Map<String, String>> _localizedValues = {
    'en': {
      'appTitle': 'KropAi',
      'hello': 'Hello',
      'login': 'Sign In',
      'email': 'Email',
      'password': 'Password',
      'myFields': 'My Fields',
      'recentScans': 'Recent Scans',
      'quickActions': 'Quick Actions',
      'scanCrop': 'Scan Crop',
      'soilAnalysis': 'Soil Analysis',
      'recommendations': 'Expert Advice',
      'history': 'History',
      'scanButton': 'SCAN CROP OR SOIL',
      'welcome': 'Welcome to NuKropAi',
      'subtitle': 'Expert farming advice in your pocket.',
      'createAccount': 'Create New Account',
      'googleSignIn': 'Continue with Google',
    },
    'hi': {
      'appTitle': 'KropAi',
      'hello': 'नमस्ते',
      'login': 'साइन इन करें',
      'email': 'ईमेल',
      'password': 'पासवर्ड',
      'myFields': 'मेरे खेत',
      'recentScans': 'हाल के स्कैन',
      'quickActions': 'त्वरित कार्रवाई',
      'scanCrop': 'फसल स्कैन',
      'soilAnalysis': 'मिट्टी विश्लेषण',
      'recommendations': 'विशेषज्ञ सलाह',
      'history': 'इतिहास',
      'scanButton': 'स्कैन करें',
      'welcome': 'KropAi में आपका स्वागत है',
      'subtitle': 'आपकी जेब में विशेषज्ञ कृषि सलाह।',
      'createAccount': 'नया खाता बनाएँ',
    },
    'te': {
      'appTitle': 'KropAi',
      'hello': 'నమస్కారం',
      'login': 'సైన్ ఇన్',
      'email': 'ఈమెయిల్',
      'password': 'పాస్‌వర్డ్',
      'myFields': 'నా పొలాలు',
      'recentScans': 'ఇటీవలి స్కాన్లు',
      'quickActions': 'త్వరిత చర్యలు',
      'scanCrop': 'పంట స్కాన్',
      'soilAnalysis': 'మట్టి విశ్లేషణ',
      'recommendations': 'నిపుణుల సలహా',
      'history': 'చరిత్ర',
      'scanButton': 'స్కాన్ చేయండి',
      'welcome': 'KropAi కి స్వాగతం',
      'subtitle': 'మీ జేబులో నిపుణుల వ్యవసాయ సలహా.',
      'createAccount': 'కొత్త ఖాతాను సృష్టించండి',
    },
  };

  String get appTitle => _localizedValues[locale.languageCode]?['appTitle'] ?? 'KropAi';
  String get hello => _localizedValues[locale.languageCode]?['hello'] ?? 'Hello';
  String get login => _localizedValues[locale.languageCode]?['login'] ?? 'Sign In';
  String get email => _localizedValues[locale.languageCode]?['email'] ?? 'Email';
  String get password => _localizedValues[locale.languageCode]?['password'] ?? 'Password';
  String get myFields => _localizedValues[locale.languageCode]?['myFields'] ?? 'My Fields';
  String get recentScans => _localizedValues[locale.languageCode]?['recentScans'] ?? 'Recent Scans';
  String get quickActions => _localizedValues[locale.languageCode]?['quickActions'] ?? 'Quick Actions';
  String get scanCrop => _localizedValues[locale.languageCode]?['scanCrop'] ?? 'Scan Crop';
  String get soilAnalysis => _localizedValues[locale.languageCode]?['soilAnalysis'] ?? 'Soil Analysis';
  String get recommendations => _localizedValues[locale.languageCode]?['recommendations'] ?? 'Expert Advice';
  String get history => _localizedValues[locale.languageCode]?['history'] ?? 'History';
  String get scanButton => _localizedValues[locale.languageCode]?['scanButton'] ?? 'SCAN CROP OR SOIL';
  String get welcome => _localizedValues[locale.languageCode]?['welcome'] ?? 'Welcome to KropAi';
  String get subtitle => _localizedValues[locale.languageCode]?['subtitle'] ?? 'Expert farming advice in your pocket.';
  String get createAccount => _localizedValues[locale.languageCode]?['createAccount'] ?? 'Create New Account';

  static const LocalizationsDelegate<AppLocalizations> delegate = _AppLocalizationsDelegate();
}

class _AppLocalizationsDelegate extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  bool isSupported(Locale locale) => ['en', 'hi', 'te', 'ta', 'kn', 'mr', 'bn'].contains(locale.languageCode);

  @override
  Future<AppLocalizations> load(Locale locale) async => AppLocalizations(locale);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}
