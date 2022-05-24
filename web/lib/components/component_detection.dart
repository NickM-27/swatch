import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/models/detection_event.dart';

class DetectionComponent extends StatelessWidget {
  final SwatchApi _api = SwatchApi();
  final DetectionEvent event;

  DetectionComponent(
    this.event, {
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.purple,
      width: double.infinity,
      child: Row(
        children: [
          Text(
            event.camera,
            style: const TextStyle(fontSize: 42.0),
          ),
          Text(event.label),
          Text(event.zone)
        ],
      ),
    );
  }
}
