import 'package:flutter/material.dart';

final ThemeData mainTheme = ThemeData(

)

class SwatchColors {
  SwatchColors._();

  static const Map<int, Color> _primary = const <int, Color>{
    50: const Color(0xFF0097a7),
    100: const Color(0xFF0097a7),
    200: const Color(0xFF0097a7),
    300: const Color(0xFF0097a7),
    400: const Color(0xFF0097a7),
    500: const Color(0xFF0097a7),
    600: const Color(0xFF0097a7),
    700: const Color(0xFF0097a7),
    800: const Color(0xFF0097a7),
    900: const Color(0xFF0097a7),
  };
  static const Map<int, Color> _accent = const {
    50: const Color(0xFFad1457),
    100: const Color(0xFFad1457),
    200: const Color(0xFFad1457),
    300: const Color(0xFFad1457),
    400: const Color(0xFFad1457),
    500: const Color(0xFFad1457),
    600: const Color(0xFFad1457),
    700: const Color(0xFFad1457),
    800: const Color(0xFFad1457),
    900: const Color(0xFFad1457),
  };

  static Color getPrimaryColor(final int shade) {
    final custom = PrefService.getInt("primary");

    if (custom != null)
      return Color(custom);
    else
      return _primary[shade];
  }

  static Color getAccentColor(final int shade) {
    final custom = PrefService.getInt('accent');

    if (custom != null)
      return Color(custom);
    else
      return _accent[shade];
  }
}