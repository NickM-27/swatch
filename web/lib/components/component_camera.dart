import 'package:flutter/material.dart';
import 'package:swatch/components/component_zone.dart';
import 'package:swatch/ext/extension_string.dart';
import 'package:swatch/models/camera.dart';

class CameraComponent extends StatelessWidget {
  final Camera camera;

  const CameraComponent(
    this.camera, {
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(8.0),
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          AspectRatio(
            aspectRatio: 2.1,
            child: Image.network(
              "http://localhost:4500/api/${camera.name}/snapshot.jpg",
              fit: BoxFit.fitWidth,
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text(
              camera.name.replaceAll('_', ' ').title(),
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.fromLTRB(8.0, 24.0, 8.0, 8.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.end,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text(
                  "Zones:",
                  style: TextStyle(fontWeight: FontWeight.bold),
                ),
                Row(
                  crossAxisAlignment: CrossAxisAlignment.end,
                  children: _getZones(camera),
                )
              ],
            ),
          )
        ],
      ),
    );
  }

  List<Widget> _getZones(Camera config) {
    final keys = config.zones.keys.toList();
    return List.generate(config.zones.length,
        (index) => ZoneComponent(config, config.zones[keys[index]]!));
  }
}
