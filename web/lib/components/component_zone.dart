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
    return SizedBox(
      height: 112.0,
      width: 112.0,
      child: Card(
        color: Colors.grey[700],
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.all(
            Radius.circular(8.0),
          ),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.max,
          mainAxisAlignment: MainAxisAlignment.end,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.all(Radius.circular(8.0)),
              child: Image.network(
                "${_api.getHost()}/api/${camera.name}/${zone.name}/snapshot.jpg",
                height: 80,
                width: 112,
                fit: BoxFit.fill,
              ),
            ),
            Padding(
              padding: const EdgeInsets.fromLTRB(8.0, 4.0, 8.0, 4.0),
              child: Text(
                zone.name.replaceAll('_', ' ').title(),
                style: const TextStyle(
                  fontSize: 14,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
