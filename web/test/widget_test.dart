// This is a basic Flutter widget test.
//
// To perform an interaction with a widget in your test, use the WidgetTester
// utility in the flutter_test package. For example, you can send tap and scroll
// gestures. You can also use WidgetTester to find child widgets in the widget
// tree, read text, and verify that the values of widget properties are correct.

import 'package:flutter_test/flutter_test.dart';

import 'package:swatch/models/config.dart';

void main() {
  final config = {
    "objects": {
      "test_obj": {
        "color_variants": {
          "default": {
            "color_lower": "1, 1, 1",
            "color_upper": "2, 2, 2",
          },
        },
        "min_area": 0,
        "max_area": 100000,
      },
    },
    "cameras": {
      "test_cam": {
        "snapshot_config": {
          "url": "http://localhost/snap.jpg",
        },
        "zones": {
          "test_zone": {
            "coordinates": "1, 2, 3, 4",
            "objects": ["test_obj"],
          },
        },
      },
    },
  };

  test("Config is parsed correctly", () {
    final swatchConfig = Config(config);
    assert(swatchConfig.cameras.isNotEmpty);
  });
}
