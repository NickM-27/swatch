import 'package:intl/intl.dart';
import 'package:swatch/ext/extension_string.dart';

class DetectionEvent {

  String id = "";
  String camera = "";
  String label = "";
  String zone = "";
  String colorVariant = "";
  int topArea = 0;
  double startTime = 0;
  double endTime = -1;

  DetectionEvent(final Map<String, dynamic> json) {
    id = json["id"] ?? "";
    camera = json["camera"] ?? "";
    label = json["label"] ?? "";
    zone = json["zone"] ?? "";
    colorVariant = json["color_variant"] ?? "";
    topArea = json["top_area"] ?? 0;
    startTime = json["start_time"] ?? 0;
    endTime = json["end_time"] ?? -1;
  }

  String getLabel() => label.replaceAll("_", " ").title();

  String getCamera() => camera.replaceAll("_", " ").title();

  String getZone() => zone.replaceAll("_", " ").title();

  String getColorVariant() => colorVariant.replaceAll("_", " ").title();

  String getTime() {
    if (endTime == -1) {
      return "In Progress";
    } else {
      final start = DateTime.fromMillisecondsSinceEpoch((startTime * 1000).toInt());
      final end = DateTime.fromMillisecondsSinceEpoch((endTime * 1000).toInt());
      final format = DateFormat("MM/dd/yyyy hh:mm");
      return "${format.format(start)} -> ${format.format(end)}";
    }
  }
}