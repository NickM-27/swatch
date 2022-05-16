import 'package:flutter/material.dart';
import 'package:swatch/ext/extension_string.dart';
import 'package:swatch/models/camera.dart';

class CameraComponent extends StatelessWidget {

  final Camera camera;

  const CameraComponent(this.camera, {Key? key,}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          Text(camera.name.replaceAll('_', ' ').title(), style: const TextStyle(fontSize: 44,),),
          Image.network("https://raw.githubusercontent.com/NickM-27/swatch/master/assets/swatch.png", width: 200.0, height: 200.0,)
        ],
      ),
    );
  }
}