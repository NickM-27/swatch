# HTTP API

## `/api/config`

Returns JSON config

## `/api/<camera_name>/detect`

```json
{
    "imageUrl": "http://some_camera_image.jpg"
}
```

Take the `camera_name` config and `imageUrl` to run detection and see which objects are detected.

## `/api/colortest`

```json
{ "test_image": test_image.jpg } // files
```

Upload image to get info about colors detected in the image.
This should make it easier to add objects with known colors as
the program sees them.
