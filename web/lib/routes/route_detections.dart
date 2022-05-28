import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/components/component_detection.dart';
import 'package:swatch/const.dart';

import 'package:collapsible_sidebar/collapsible_sidebar.dart';
import 'package:swatch/models/detection_event.dart';
import 'package:swatch/theme/theme_helper.dart';

class DetectionListRoute extends StatefulWidget {
  static const String route = '/detections';

  const DetectionListRoute({Key? key}) : super(key: key);

  @override
  DetectionListRouteState createState() => DetectionListRouteState();
}

class DetectionListRouteState extends State<DetectionListRoute> {
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
                items: getSidebarRoutes(context, DetectionListRoute.route),
                avatarImg: const NetworkImage(
                  "https://raw.githubusercontent.com/NickM-27/swatch/master/assets/swatch.png",
                ),
                body: _DetectionsView(),
                backgroundColor: Colors.blueGrey[700]!,
                selectedTextColor: SwatchColors.getPrimaryColor(),
                iconSize: 24,
                borderRadius: 12,
                sidebarBoxShadow: const [],
                title: "Swatch",
                textStyle: const TextStyle(
                  fontSize: 16,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _DetectionsView extends StatefulWidget {
  @override
  State<_DetectionsView> createState() => _DetectionsViewState();
}

class _DetectionsViewState extends State<_DetectionsView> {
  final SwatchApi _api = SwatchApi();

  late Future<List<DetectionEvent>> _detections;

  @override
  void initState() {
    super.initState();
    _detections = _api.getDetections();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: FutureBuilder(
        future: _detections,
        builder: (context, AsyncSnapshot<List<DetectionEvent>> detections) {
          if (detections.hasData && detections.data!.isNotEmpty) {
            return ListView(
              children: _getDetections(detections.data!),
            );
          } else {
            return Container(
              alignment: Alignment.center,
              child: const SizedBox(
                width: 400.0,
                child: Text(
                  "No detections found. Once an object is detected it will appear here.",
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 24.0),
                ),
              ),
            );
          }
        },
      ),
    );
  }

  List<Widget> _getDetections(List<DetectionEvent> detections) {
    return detections.map((e) => DetectionComponent(e, onDeleted)).toList();
  }

  onDeleted() {
    final update = _api.getDetections();
    setState(() {
      _detections = update;
    });
  }
}
