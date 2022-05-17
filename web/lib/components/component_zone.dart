import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/ext/extension_string.dart';
import 'package:swatch/models/camera.dart';
import 'package:swatch/models/zone.dart';

class ZoneComponent extends StatelessWidget {

  final SwatchApi _api = SwatchApi();
  final Camera camera;
  final Zone zone;

  ZoneComponent(
    this.camera,
    this.zone, {
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
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Image.network(
            "${_api.getHost()}/api/${camera.name}/${zone.name}/snapshot.jpg",
            height: 100,
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text(
              zone.name.replaceAll('_', ' ').title(),
              style: const TextStyle(
                fontSize: 14,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
