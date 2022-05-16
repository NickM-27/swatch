import 'package:swatch/models/zone.dart';

class Camera {

  String name = "";
  int autoDetect = 0;
  Map<String, Zone> zones = {};

  Camera(final Map<String, dynamic> json) {
    name = json["name"];
    autoDetect = json["auto_detect"];

    json["zones"].forEach((name, json) {
      Zone zone = Zone(json);
      zone.name = name;
      zones[name] = zone;
    });
  }
}