import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/components/component_camera.dart';
import 'package:swatch/models/config.dart';

class DashboardRoute extends StatefulWidget {
  const DashboardRoute({Key? key}) : super(key: key);

  @override
  DashboardRouteState createState() => DashboardRouteState();
}

class DashboardRouteState extends State<DashboardRoute> {
  final SwatchApi _api = SwatchApi();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder(
        future: _api.getConfig(),
        builder: (context, AsyncSnapshot<Config> config) {
          if (config.hasData) {
            return GridView.extent(
              childAspectRatio: 1,
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
