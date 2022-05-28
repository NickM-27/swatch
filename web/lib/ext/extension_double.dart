extension IntExtension on double {

  int getColumnsForWidth() {
    if (this < 600) {
      return 1;
    } else if (this < 1200) {
      return 2;
    } else if (this < 1800) {
      return 3;
    } else {
      return 4;
    }
  }
}