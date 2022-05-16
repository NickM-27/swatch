import 'package:flutter/material.dart';
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
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Image.network(
            "http://localhost:4500/api/${camera.name}/snapshot.jpg",
            height: 260,
            width: double.infinity,
            fit: BoxFit.fitWidth,
          ),
          Padding(
            padding: const EdgeInsets.all(8.0),
            child: Text(
              camera.name.replaceAll('_', ' ').title(),
              style: const TextStyle(
                fontSize: 24,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
