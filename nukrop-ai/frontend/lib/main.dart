import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:hive_flutter/hive_flutter.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:nukrop_ai/features/dashboard/dashboard_screen.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  await Hive.openBox('farm_memory_box'); // Local History Database Initialization
  await dotenv.load(fileName: ".env"); // Load safety layer

  runApp(const ProviderScope(child: NuKropOS()));
}

class NuKropOS extends StatelessWidget {
  const NuKropOS({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'NuKrop Agri-OS',
      themeMode: ThemeMode.dark, // Standardize on Premium Dark
      darkTheme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF0F172A), // Dark Slate
        colorScheme: ColorScheme.dark(primary: const Color(0xFF0FCE7D)),
        textTheme: ThemeData.dark().textTheme.apply(fontFamily: 'Roboto'),
      ),
      home: const DashboardScreen(),
    );
  }
}