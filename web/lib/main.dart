import 'package:flutter/material.dart';
import 'package:swatch/components/component_nav.dart';
import 'package:swatch/theme/theme_helper.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Swatch',
      theme: mainTheme,
      debugShowCheckedModeBanner: false,
      home: const NavStructure(),
    );
  }
}
