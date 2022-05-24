import 'package:flutter/material.dart';
import 'package:swatch/api/api.dart';
import 'package:swatch/models/detection_event.dart';

class DetectionComponent extends StatelessWidget {
  final SwatchApi _api = SwatchApi();
  final DetectionEvent event;

  DetectionComponent(
    this.event, {
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Container(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          children: [
            ClipRRect(
              borderRadius: const BorderRadius.all(Radius.circular(8.0)),
              child: Image.network(
                "${_api.getHost()}/api/detections/${event.id}/snapshot.jpg",
                height: 100.0,
                fit: BoxFit.fill,
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    "${event.getLabel()} (${event.topArea} px)",
                    textAlign: TextAlign.start,
                    style: const TextStyle(
                      fontSize: 18.0,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                  Text(event.getTime()),
                  const SizedBox(height: 32.0),
                  Row(
                    children: [
                      Wrap(
                        crossAxisAlignment: WrapCrossAlignment.center,
                        children: [
                          const Icon(Icons.video_camera_back_outlined),
                          Padding(
                            padding:
                                const EdgeInsets.symmetric(horizontal: 4.0),
                            child: Text(
                              event.getCamera(),
                              textAlign: TextAlign.center,
                            ),
                          )
                        ],
                      ),
                      Wrap(
                        crossAxisAlignment: WrapCrossAlignment.center,
                        children: [
                          const Icon(Icons.location_on_outlined),
                          Text(
                            event.getZone(),
                            textAlign: TextAlign.center,
                          )
                        ],
                      )
                    ],
                  ),
                ],
              ),
            ),
            const Spacer(),
            Column(
              children: [],
            ),
          ],
        ),
      ),
    );
  }
}
