

import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';

class DashboardRoute extends StatefulWidget {

  const DashboardRoute({Key? key}) : super(key: key);

  @override
  DashboardRouteState createState() => DashboardRouteState();
}

class DashboardRouteState extends State<DashboardRoute> {

  final SwatchApi _api = SwatchApi();

  @override
  void initState() {
    super.initState();
    _api.getConfig();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: const Text("Selected Dashboard"),
    );
  }
}