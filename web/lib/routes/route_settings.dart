import 'dart:html' as html;

import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/routes/route_color_playground.dart';
import 'package:swatch/routes/route_dashboard.dart';
import 'package:swatch/theme/theme_helper.dart';
import 'package:swatch/const.dart';

class SettingsRoute extends StatefulWidget {
  static const String route = '/settings';

  const SettingsRoute({Key? key}) : super(key: key);

  @override
  SettingsRouteState createState() => SettingsRouteState();
}

class SettingsRouteState extends State<SettingsRoute> {
  late List<CollapsibleItem> _routes;

  @override
  void initState() {
    super.initState();
    _routes = _generateRoutes;
  }

  List<CollapsibleItem> get _generateRoutes {
    return [
      CollapsibleItem(
        text: "Dashboard",
        icon: Icons.dashboard_outlined,
        onPressed: () =>
            Navigator.of(context).pushReplacementNamed(DashboardRoute.route),
      ),
      CollapsibleItem(
        text: "Color Playground",
        icon: Icons.colorize_outlined,
        onPressed: () => Navigator.of(context)
            .pushReplacementNamed(ColorPlaygroundRoute.route),
      ),
      CollapsibleItem(
        text: "Settings",
        icon: Icons.settings_outlined,
        isSelected: true,
        onPressed: () {},
      ),
      CollapsibleItem(
        text: "GitHub",
        icon: Icons.code,
        isSelected: false,
        onPressed: () => html.window.open(urlGitHubReadme, "swatch-readme"),
      ),
      CollapsibleItem(
        text: "Docs",
        icon: Icons.mark_chat_read_outlined,
        isSelected: false,
        onPressed: () => html.window.open(urlGitHubDocs, "swatch-docs"),
      ),
    ];
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Swatch"),
        centerTitle: false,
        backgroundColor: SwatchColors.getPrimaryColor(),
      ),
      body: SafeArea(
        child: Stack(
          children: [
            Align(
              alignment: Alignment.centerLeft,
              child: CollapsibleSidebar(
                isCollapsed: true,
                items: _routes,
                avatarImg: const NetworkImage(
                  "https://raw.githubusercontent.com/NickM-27/swatch/master/assets/swatch.png",
                ),
                body: _SettingsView(),
                backgroundColor: Colors.blueGrey[700]!,
                selectedTextColor: SwatchColors.getPrimaryColor(),
                iconSize: 24,
                borderRadius: 12,
                sidebarBoxShadow: const [],
                title: "Swatch",
                textStyle: const TextStyle(
                  fontSize: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SettingsView extends StatelessWidget {
  final SwatchApi _api = SwatchApi();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        alignment: Alignment.center,
        child: const Text("Settings will be added later"),
      ),
    );
  }
}
