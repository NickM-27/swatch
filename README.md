<!-- markdownlint-disable first-line-heading -->
<!-- markdownlint-disable no-inline-html -->

<img src="https://raw.githubusercontent.com/NickM-27/swatch/master/assets/swatch.png"
     alt="Swatch icon"
     width="16%"
     align="right"
     style="float: right; margin: 10px 0px 20px 20px;" />

[![GitHub Release](https://img.shields.io/github/release/NickM-27/swatch.svg?style=flat-square)](https://github.com/NickM-27/swatch/releases)
[![Build Status](https://img.shields.io/github/workflow/status/NickM-27/swatch/Build?style=flat-square)](https://github.com/NickM-27/swatch/actions/workflows/build.yaml)
[![License](https://img.shields.io/github/license/NickM-27/swatch.svg?style=flat-square)](LICENSE)

# swatch

Color detection in images to capture presence of known objects.

## Why?

There is great object and face detection software out there, but sometimes AI detection is overkill or not suitable different types of objects. Swatch was created to create an easy to use API to detect the presence of objects of known color in expected places.

In this example you can see a cropped section of the street with a trash can. Then, using expected color bounds, the parts of the image that don't match the expected color are masked away. If a significant enough amount of pixels are left that match the color then it can be considered a true positive.

![crop](https://user-images.githubusercontent.com/14866235/160126079-14dd083c-7ca8-4077-882c-3f5eddeaf6a0.jpg)
![crop-mask](https://user-images.githubusercontent.com/14866235/160126093-82cedb91-c04e-44a2-8f0f-154e084f2f8f.jpg)

## Features

- REST API to be invoked by other applications

## Configuration

A `config.yaml` file must be created and mapped to `/opt/swatch/config/`

### `objects`

```yaml
# REQUIRED: Define a list of objects that are expected to be seen. These can be specific
# to one camera or common between many / all cameras
objects:
  # REQUIRED: Name of the object
  trash_can:
    # REQUIRED: the lower R, G, B values that are considered a potential match for the object.
    color_lower: 70, 70, 0
    # REQUIRED: the upper R, G, B values that are considered a potential match for the object.
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

## API References

Check out [GitHub Docs](docs/api.md) for the API reference.

## Contributing

**Contributions are very much welcome!**

For instructions on how to get started, see the [contributing section](CONTRIBUTING.md)

### Donations

If you would like to make a donation to support development, please use [GitHub Sponsors](https://github.com/sponsors/NickM-27).
