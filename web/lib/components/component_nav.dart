import 'package:flutter/material.dart';
import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:web/routes/route_dashboard.dart';
import 'package:web/theme/theme_helper.dart';

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
    ];
  }

  @override
  Widget build(BuildContext context) {
    return CollapsibleSidebar(
      isCollapsed: true,
      items: _routes,
      avatarImg: const AssetImage("swatch.png"),
      body: _getCurrentRoute(),
      backgroundColor: Colors.blueGrey[700]!,
      selectedTextColor: SwatchColors.getPrimaryColor(),
      maxWidth: 100,
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
