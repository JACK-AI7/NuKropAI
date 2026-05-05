import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppColors {
  // Dark Farm Palette (Image 1)
  static const Color background = Color(0xFF0F172A);
  static const Color darkGreen = Color(0xFF064E3B);
  static const Color glassWhite = Color(0x1AFFFFFF);
  static const Color glassBorder = Color(0x33FFFFFF);
  
  // Minimalist Data Palette (Image 2)
  static const Color whiteCard = Colors.white;
  static const Color offWhite = Color(0xFFF1F5F9);
  static const Color textDark = Color(0xFF0F172A);
  static const Color textGrey = Color(0xFF64748B);
  
  static const Color accent = Color(0xFF4CAF50); 
  static const Color secondaryAccent = Color(0xFF10B981); // Emerald
  
  // Compatibility Aliases
  static const Color primary = Color(0xFF4CAF50);
  static const Color textPrimary = Color(0xFF0F172A);
  static const Color textSecondary = Color(0xFF64748B);

  static BoxDecoration glassDecoration({double radius = 24, bool highlight = false}) {
    return BoxDecoration(
      color: highlight ? Colors.white.withOpacity(0.2) : Colors.white.withOpacity(0.1),
      borderRadius: BorderRadius.circular(radius),
      border: Border.all(color: Colors.white.withOpacity(0.2), width: 1.5),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withOpacity(0.1),
          blurRadius: 20,
          spreadRadius: -5,
        )
      ],
    );
  }
}


class AppTheme {
  static ThemeData get hybridTheme {
    return ThemeData(
      brightness: Brightness.dark,
      primaryColor: AppColors.accent,
      scaffoldBackgroundColor: AppColors.background,
      textTheme: GoogleFonts.outfitTextTheme(const TextTheme(
        headlineLarge: TextStyle(fontSize: 48, fontWeight: FontWeight.w800, color: Colors.white, letterSpacing: -1.5),
        headlineMedium: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
        titleLarge: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: Colors.white),
        bodyLarge: TextStyle(fontSize: 16, color: Colors.white),
        bodyMedium: TextStyle(fontSize: 14, color: Colors.white70),
      )),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: AppColors.accent,
          foregroundColor: Colors.white,
          elevation: 0,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          padding: const EdgeInsets.symmetric(vertical: 18),
        ),
      ),
      cardTheme: CardThemeData(
        color: AppColors.whiteCard,
        elevation: 0,
        shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24)),
      ),
    );
  }
}
