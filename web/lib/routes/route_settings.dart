
import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/theme/theme_helper.dart';
import 'package:swatch/const.dart';

class SettingsRoute extends StatefulWidget {
  static const String route = '/settings';

  const SettingsRoute({Key? key}) : super(key: key);

  @override
  SettingsRouteState createState() => SettingsRouteState();
}

class SettingsRouteState extends State<SettingsRoute> {

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
                items: getSidebarRoutes(context, SettingsRoute.route),
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
