import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:swatch/models/config.dart';
import 'package:window_location_href/window_location_href.dart';

class SwatchApi {
  static final SwatchApi _singleton = SwatchApi._internal();
  static String _swatchHost = "";

  factory SwatchApi() {
    if (kDebugMode) {
      _swatchHost = "localhost:4500";
    } else {
      final location = (getHref() ?? "").replaceAll("http://", "");
      _swatchHost = location.substring(0, location.indexOf("/"));
    }

    return _singleton;
  }

  SwatchApi._internal();

  String getHost() => Uri.http(_swatchHost, "").toString();

  /// Swatch API Funs

  Future<Config> getConfig() async {
    const base = "/api/config";
    final response = await http.get(Uri.http(_swatchHost, base)).timeout(
          const Duration(seconds: 15),
        );

    if (response.statusCode == 200) {
      return Config(json.decode(response.body));
    } else {
      return Config.template();
    }
  }

  Future<Config> getLatest() async {
    const base = "/api/all/latest";
    final response = await http.get(Uri.http(_swatchHost, base)).timeout(
      const Duration(seconds: 15),
    );

    if (response.statusCode == 200) {
      return Config(json.decode(response.body));
    } else {
      return Config.template();
    }
  }

  /// General Utility Funs

  Future<Uint8List> getImageBytes(final String imageSource) async {
    try {
      final http.Response r = await http.get(
        Uri.parse(imageSource),
      );
      return r.bodyBytes;
    } catch (e) {
      return Uint8List(0);
    }
  }
}
