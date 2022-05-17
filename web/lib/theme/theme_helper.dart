import 'package:flutter/material.dart';

final ThemeData mainTheme = ThemeData(
  primaryColor: SwatchColors.getPrimaryColor(),
  primaryColorLight: SwatchColors.getPrimaryColor(),
  primaryColorDark: SwatchColors.getPrimaryColor(),
  iconTheme: ThemeData.dark().iconTheme,
  bottomAppBarColor: SwatchColors.getAccentColor(),
  brightness: Brightness.dark,
  backgroundColor: Colors.blueGrey[700]!,
);

class SwatchColors {
  SwatchColors._();

  static const Map<int, Color> _primary = <int, Color>{
    50: Color(0xFF62B8Bf),
    100: Color(0xFF62B8Bf),
    200: Color(0xFF62B8Bf),
    300: Color(0xFF62B8Bf),
    400: Color(0xFF62B8Bf),
    500: Color(0xFF62B8Bf),
    600: Color(0xFF62B8Bf),
    700: Color(0xFF62B8Bf),
    800: Color(0xFF62B8Bf),
    900: Color(0xFF62B8Bf),
  };
  static const Map<int, Color> _accent = {
    50: Color(0xFFad1457),
    100: Color(0xFFad1457),
    200: Color(0xFFad1457),
    300: Color(0xFFad1457),
    400: Color(0xFFad1457),
    500: Color(0xFFad1457),
    600: Color(0xFFad1457),
    700: Color(0xFFad1457),
    800: Color(0xFFad1457),
    900: Color(0xFFad1457),
  };

  static Color getPrimaryColor() => _primary[50]!;

  static Color getAccentColor() => _accent[50]!;
}
