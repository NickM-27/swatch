class DetectionEvent {

  String id = "";
  String camera = "";
  String label = "";
  String zone = "";
  String colorVariant = "";
  int topArea = 0;
  int startTime = 0;
  int endTime = -1;

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
}