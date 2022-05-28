import 'package:flutter/material.dart';
import 'package:swatch/theme/theme_helper.dart';

class CreateZoneComponent extends StatelessWidget {
  const CreateZoneComponent({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Colors.grey[700],
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.all(
          Radius.circular(8.0),
        ),
      ),
      child: Expanded(
        child: IconButton(
          icon: Icon(
            Icons.add_location_alt_outlined,
            color: SwatchColors.getPrimaryColor(),
          ),
          onPressed: () {},
        ),
      ),
    );
  }
}
