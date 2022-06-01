import 'package:flutter/material.dart';
import 'package:flutter_layout_grid/flutter_layout_grid.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/components/component_camera.dart';
import 'package:swatch/const.dart';
import 'package:swatch/ext/extension_double.dart';
import 'package:swatch/models/config.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/theme/theme_helper.dart';

class DashboardRoute extends StatefulWidget {
  static const String route = '/dashboard';

  const DashboardRoute({Key? key}) : super(key: key);

  @override
  DashboardRouteState createState() => DashboardRouteState();
}

class DashboardRouteState extends State<DashboardRoute> {
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
                items: getSidebarRoutes(context, DashboardRoute.route),
                avatarImg: const NetworkImage(
                  "https://raw.githubusercontent.com/NickM-27/swatch/master/assets/swatch.png",
                ),
                body: _DashboardView(),
                backgroundColor: Colors.blueGrey[700]!,
                selectedTextColor: SwatchColors.getPrimaryColor(),
                iconSize: 24,
                borderRadius: 12,
                duration: const Duration(seconds: 0),
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

class _DashboardView extends StatefulWidget {
  @override
  State<_DashboardView> createState() => _DashboardViewState();
}

class _DashboardViewState extends State<_DashboardView> {
  final SwatchApi _api = SwatchApi();

  @override
  Widget build(BuildContext context) {
    final columnCount = MediaQuery.of(context).size.width.getColumnsForWidth();

    return Scaffold(
      body: FutureBuilder(
        future: _api.getConfig(),
        builder: (context, AsyncSnapshot<Config> config) {
          if (config.hasData) {
            return LayoutGrid(
              columnSizes: List.generate(columnCount, (index) => 1.fr),
              rowSizes: List.generate(columnCount, (index) => auto),
              children: _getCameras(config.data!),
            );
          } else {
            return Container();
          }
        },
      ),
    );
  }

  List<Widget> _getCameras(Config config) {
    final keys = config.cameras.keys.toList();
    return List.generate(config.cameras.length,
        (index) => CameraComponent(config.cameras[keys[index]]!));
  }
}
