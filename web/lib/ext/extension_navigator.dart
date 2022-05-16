import 'package:flutter/material.dart';
import 'package:swatch/routes/route_color_playground.dart';
import 'package:swatch/routes/route_dashboard.dart';

extension NavigatorExtension on NavigatorState {
  static final Map<String, Widget> _routeMap = {
    DashboardRoute.route: const DashboardRoute(),
    ColorPlaygroundRoute.route: const ColorPlaygroundRoute(),
  };

  void openRoute(final String route) {
    pushReplacement(
      PageRouteBuilder(
        pageBuilder: (context, a1, a2) => _routeMap[route]!,
        transitionDuration: const Duration(seconds: 0),
      ),
    );
  }
}
