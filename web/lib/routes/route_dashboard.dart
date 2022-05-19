import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/components/component_camera.dart';
import 'package:swatch/models/config.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/routes/route_color_playground.dart';
import 'package:swatch/theme/theme_helper.dart';

class DashboardRoute extends StatefulWidget {

  static const String route = '/dashboard';

  const DashboardRoute({Key? key}) : super(key: key);

  @override
  DashboardRouteState createState() => DashboardRouteState();
}

class DashboardRouteState extends State<DashboardRoute> {

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
        isSelected: true,
        onPressed: () {},
      ),
      CollapsibleItem(
        text: "Color Playground",
        icon: Icons.colorize_outlined,
        onPressed: () => Navigator.of(context).pushReplacementNamed(ColorPlaygroundRoute.route),
      ),
      /*CollapsibleItem(
        text: "Settings",
        icon: Icons.settings_outlined,
        onPressed: () => Navigator.of(context).pushReplacementNamed(SettingsRoute.route),
      ),*/
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
                body: _DashboardView(),
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

class _DashboardView extends StatelessWidget {

  final SwatchApi _api = SwatchApi();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder(
        future: _api.getConfig(),
        builder: (context, AsyncSnapshot<Config> config) {
          if (config.hasData) {
            return GridView.extent(
              maxCrossAxisExtent: 500,
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
