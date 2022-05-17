class Detectable {

  int minArea = 0;
  int maxArea = 0;

  Detectable(final Map<String, dynamic> json) {
    minArea = json["min_area"];
    maxArea = json["max_area"];
  }
}