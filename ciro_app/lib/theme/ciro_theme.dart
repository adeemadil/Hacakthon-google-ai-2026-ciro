import 'package:flutter/material.dart';

class CiroTheme {
  static ThemeData get darkTheme {
    return ThemeData(
      brightness: Brightness.dark,
      primaryColor: Colors.red[700],
      scaffoldBackgroundColor: const Color(0xFF0d0d1e),
      cardColor: const Color(0xFF1a1a2e),
      colorScheme: const ColorScheme.dark(
        primary: Color(0xFFD32F2F), // Colors.red[700]
        secondary: Colors.redAccent,
        surface: Color(0xFF1A1A2E),
        background: Color(0xFF0D0D1E),
      ),
      appBarTheme: const AppBarTheme(
        backgroundColor: Color(0xFF0D0D1E),
        elevation: 0,
        centerTitle: true,
        titleTextStyle: TextStyle(
          color: Colors.white,
          fontSize: 20,
          fontWeight: FontWeight.bold,
          letterSpacing: 1.2,
        ),
      ),
      cardTheme: const CardTheme(
        color: Color(0xFF1A1A2E),
        elevation: 4,
        margin: EdgeInsets.all(8),
      ),
    );
  }
}
