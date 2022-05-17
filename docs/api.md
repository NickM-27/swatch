# HTTP API

## `/api/config`

Returns JSON config

## `/api/colortest/values`

```json
{ "test_image": test_image.jpg } // multipart file
```

Upload image to get info about colors detected in the image.
This should make it easier to add objects with known colors as
the program sees them.

## `/api/colortest/mask`

```json
{ "test_image": test_image.jpg } // multipart file
{
    "color_lower": "0, 0, 0",
    "color_upper": "255, 255, 255"
} // fields
```

Upload image to get info about colors detected in the image.
This should make it easier to add objects with known colors as
the program sees them.

## `/api/<camera_name>/detect`

```json
{
    "imageUrl": "http://some_camera_image.jpg"
}
```

Take the `camera_name` config and `imageUrl` to run detection and see which objects are detected.

## `/api/<label>/latest`

Returns the latest results for the given label. `all` can be passed to get a result for all labels.

```json
{
    "trash_can":{
        "area":2818,
        "camera_name":"front_doorbell_cam",
        "result":true,
        "variant":"overcast"
    }
}
```

## `/api/<camera_name>/snapshot.jpg`

Returns a snapshot of the latest image for the <camera_name>.

## `/api/<camera_name>/<zone_name>/snapshot.jpg`

Returns a snapshot of the latest snapshot for the <zone_name> of the <camera_name>.

## `/api/<camera_name>/detection.jpg`

Returns a snapshot of the latest detection for the <camera_name>.
