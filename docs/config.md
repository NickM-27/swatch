# Config

Setting up the config requires two main sections. Objects are used to define the different objects that swatch can detect, and cameras are used to define the common image producers that will be used.

## `objects`

```yaml
# REQUIRED: Define a list of objects that are expected to be seen. These can be specific
# to one camera or common between many / all cameras
objects:
  # REQUIRED: Name of the object
  trash_can:
    # REQUIRED: the list of color variants that this object can be detected as. Useful for
    # different lighting conditions
    color_variants:
      # REQUIRED: the name of the color variant
      default:
        # REQUIRED: the lower R, G, B values that are considered a potential match for the
        # color variant of the object.
        color_lower: 70, 70, 0
        # REQUIRED: the upper R, G, B values that are considered a potential match for the
        # color variant of the object.
        color_upper: 110, 100, 50
    # OPTIONAL: the min number of pixels with R, G, B values within the bounds to be
    # considered a true positive. This is recommended to be set as a super small amount
    # could be a false positive. (Default: shown below)
    min_area: 1000
    # OPTIONAL: the max number of pixels with R, G, B values within the bounds to be
    # considered a true positive (Default: shown below).
    max_area: 100000
```

### `cameras`

```yaml
# REQUIRED: Define list of cameras that will be used for color detection.
cameras:
  # REQUIRED: Name of the camera
  front_doorbell_cam:
    # OPTIONAL: but highly recommended, setting the default url for a snapshot to be
    # processed by this camera. This is required for auto detection (Default: none).
    snapshot_url: "http://ip.ad.dr.ess/jpg"
    # OPTIONAL: Frequency in seconds to run detection on the camera.
    # a value of 0 disables auto detection (Default: shown below).
    auto_detect: 0
    # REQUIRED: Zones are cropped areas where the object can be expected to be.
    # This makes searching / matches for efficient and more predictable than searching
    # the entire image.
    zones:
      # REQUIRED: Name of the zone.
      street:
        # REQUIRED: Coordinates to crop the zone by.
        coordinates: 225, 540, 350, 620
        # REQUIRED: List of objects that may be in this zone. These correspond to
        # the objects list defined previously and are matched by name.
        objects:
          - trash_can
```
