class Camera {

  String name = "";
  int autoDetect = 0;

  Camera(final Map<String, dynamic> json) {
    name = json["name"];
    autoDetect = json["auto_detect"];
  }
}