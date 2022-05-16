import 'package:flutter/material.dart';
import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/routes/route_dashboard.dart';
import 'package:swatch/theme/theme_helper.dart';

class NavStructure extends StatefulWidget {
  const NavStructure({Key? key}) : super(key: key);

  @override
  NavStructureState createState() => NavStructureState();
}

class NavStructureState extends State<NavStructure> {
  late List<CollapsibleItem> _routes;
  late String _currentRoute;

  @override
  void initState() {
    super.initState();
    _routes = _generateRoutes;
    _currentRoute = _routes.firstWhere((route) => route.isSelected).text;
  }

  List<CollapsibleItem> get _generateRoutes {
    return [
      CollapsibleItem(
        text: "Dashboard",
        icon: Icons.dashboard_outlined,
        isSelected: true,
        onPressed: () => setState(() => _currentRoute = "Dashboard"),
      ),
      CollapsibleItem(
        text: "Color Playground",
        icon: Icons.colorize_outlined,
        onPressed: () => setState(() => _currentRoute = "Color Playground"),
      ),
      CollapsibleItem(
        text: "Settings",
        icon: Icons.settings_outlined,
        onPressed: () => setState(() => _currentRoute = "Settings"),
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
                avatarImg: const AssetImage(
                  'favicon.png',
                ),
                body: _getCurrentRoute(),
                backgroundColor: Colors.blueGrey[700]!,
                selectedTextColor: SwatchColors.getPrimaryColor(),
                iconSize: 24,
                borderRadius: 12,
                sidebarBoxShadow: const [],
                title: "Swatch",
                textStyle: TextStyle(
                  fontSize: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _getCurrentRoute() {
    switch (_currentRoute) {
      case "Dashboard":
        return const DashboardRoute();
      case "Color Playground":
        return const DashboardRoute();
      default:
        throw "Not a valid route";
    }
  }
}
