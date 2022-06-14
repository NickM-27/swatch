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
        # OPTIONAL: the time range for when this color variant is allowed
        # NOTE: make sure that /etc/localtime is passed to the container so it has valid time
        time_range:
          # OPTIONAL: Color variant is valid if current time is > this 24H time (Default: shown below).
          after: "00:00"
          # OPTIONAL: Color variant is valid if current time is < this 24H time (Default: shown below).
          before: "24:00"
    # OPTIONAL: the min area of the bounding box around groups of matching R, G, B pixels
    # considered a true positive. This is not recommended to be set as a super small amount
    # could be a false positive. (Default: shown below)
    min_area: 1000
    # OPTIONAL: the max area of the bounding box around groups of pixels with R, G, B
    # values within the bounds to be considered a true positive (Default: shown below).
    max_area: 100000
    # OPTIONAL: the min ratio of width/height of bounding box for valid object detection (default: shown below).
    min_ratio: 0
     # OPTIONAL: the max ratio of width/height of bounding box for valid object detection (default: shown below).
    max_ratio: 24000000
```

### `cameras`

```yaml
# REQUIRED: Define list of cameras that will be used for color detection.
cameras:
  # REQUIRED: Name of the camera
  front_doorbell_cam:
    # OPTIONAL: Frequency in seconds to run detection on the camera.
    # a value of 0 disables auto detection (Default: shown below).
    auto_detect: 0
    # OPTIONAL: Configure the url and retention of snapshots. (Default: Shown Below)
    snapshot_config:
        # OPTIONAL: but highly recommended, setting the default url for a snapshot to be
        # processed by this camera. This is required for auto detection (Default: none).
        url: "http://ip.ad.dr.ess/jpg"
        # OPTIONAL: Whether or not to draw bounding boxes for confirmed objects in the snapshots (Default: shown below).
        bounding_box: true
        # OPTIONAL: Whether or not to save a clean png of the snapshot along with the annotated jpg (Default: shown below).
        clean_snapshot: true
        # OPTIONAL: Whether or not to save the snapshots of confirmed detections (Default: shown below).
        save_detections: true
        # OPTIONAL: Whether or not to save the snapshots of missed detections (Default: shown below).
        save_misses: false
        # OPTIONAL: Variations of snapshots to keep. Options are all, mask, crop (Default: shown below).
        mode: "all"
        # OPTIONAL: Number of days of snapshots to keep (Default: shown below).
        retain_days: 7
    # REQUIRED: Zones are cropped areas where the object can be expected to be.
    # This makes searching / matches for efficient and more predictable than searching
    # the entire image.
    zones:
      # REQUIRED: Name of the zone.
      street:
        # REQUIRED: Coordinates to crop the zone by.
        # NOTE: The order of the coordinates are: x, y, x+w, y+h starting in the top left corner as 0, 0.
        coordinates: 225, 540, 350, 620
        # REQUIRED: List of objects that may be in this zone. These correspond to
        # the objects list defined previously and are matched by name.
        objects:
          - trash_can
```
