import 'package:flutter/material.dart';

class CreateZoneComponent extends StatelessWidget {
  const CreateZoneComponent({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 112.0,
      width: 112.0,
      child: Card(
        color: Colors.grey[700],
        shape: const RoundedRectangleBorder(
          borderRadius: BorderRadius.all(
            Radius.circular(8.0),
          ),
        ),
        child: IconButton(
          icon: const Icon(
            Icons.add_location_alt_outlined,
            size: 48.0,
          ),
          onPressed: () {},
        ),
      ),
    );
  }
}
