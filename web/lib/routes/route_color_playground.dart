import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/routes/route_dashboard.dart';
import 'package:swatch/routes/route_settings.dart';
import 'package:swatch/theme/theme_helper.dart';

class ColorPlaygroundRoute extends StatefulWidget {
  static const String route = '/color_playground';

  const ColorPlaygroundRoute({Key? key}) : super(key: key);

  @override
  ColorPlaygroundRouteState createState() => ColorPlaygroundRouteState();
}

class ColorPlaygroundRouteState extends State<ColorPlaygroundRoute> {
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
        isSelected: true,
        onPressed: () {},
      ),
      CollapsibleItem(
        text: "Settings",
        icon: Icons.settings_outlined,
        onPressed: () =>
            Navigator.of(context).pushReplacementNamed(SettingsRoute.route),
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
                body: _ColorPlaygroundView(),
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

class _ColorPlaygroundView extends StatelessWidget {
  final SwatchApi _api = SwatchApi();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        alignment: Alignment.center,
        child: const Text("Big Booty"),
      ),
    );
  }
}
