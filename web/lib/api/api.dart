import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:swatch/models/config.dart';

class SwatchApi {
  static final SwatchApi _singleton = SwatchApi._internal();
  static const _swatchHost = "localhost:4500";

  factory SwatchApi() {
    return _singleton;
  }

  SwatchApi._internal();

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
}
