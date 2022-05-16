import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

class SwatchApi {
  static final SwatchApi _singleton = SwatchApi._internal();
  static final _swatch_host = "http://localhost:4501";

  factory SwatchApi() {
    return _singleton;
  }

  SwatchApi._internal();

  Future<Map<String, Object>> getConfig() async {
    const base = "/config";
    print("Calling ${Uri.http(_swatch_host, base)}");
    final response = await http.post(Uri.http(_swatch_host, base)).timeout(
          const Duration(seconds: 15),
        );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      print("We have the response $data");
      return data;
    } else {
      print("We have the error for config ${response}");
      return {};
    }
  }
}
