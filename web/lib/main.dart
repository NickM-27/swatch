import 'package:flutter/material.dart';
import 'package:swatch/ext/url_strategy/extension_url_strategy.dart';
import 'package:swatch/routes/route_color_playground.dart';
import 'package:swatch/routes/route_dashboard.dart';
import 'package:swatch/routes/route_detections.dart';
import 'package:swatch/routes/route_settings.dart';
import 'package:swatch/theme/theme_helper.dart';

void main() {
  usePathUrlStrategy();
  runApp(const SwatchApp());
}

class SwatchApp extends StatelessWidget {

  static final Map<String, Widget> _routeMap = {
    DashboardRoute.route: const DashboardRoute(),
    DetectionListRoute.route: const DetectionListRoute(),
    ColorPlaygroundRoute.route: const ColorPlaygroundRoute(),
    SettingsRoute.route: const SettingsRoute(),
  };

  const SwatchApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Swatch',
      theme: mainTheme,
      debugShowCheckedModeBanner: false,
      initialRoute: DashboardRoute.route,
      onGenerateRoute: (settings) {
        // Removes the animation from the routing
        if (_routeMap.keys.contains(settings.name)) {
          return PageRouteBuilder(
            pageBuilder: (context, a1, a2) => _routeMap[settings.name]!,
            settings: RouteSettings(name: settings.name),
            transitionDuration: const Duration(seconds: 0),
          );
        }

        return null;
      },
    );
  }
}
