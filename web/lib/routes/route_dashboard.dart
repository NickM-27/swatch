

import 'package:flutter/material.dart';
import 'package:web/theme/theme_helper.dart';

class DashboardRoute extends StatefulWidget {

  const DashboardRoute({Key? key}) : super(key: key);

  @override
  DashboardRouteState createState() => DashboardRouteState();
}

class DashboardRouteState extends State<DashboardRoute> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: const Text("Selected Dashboard"),
    );
  }
}