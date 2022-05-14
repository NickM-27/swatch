# Finding Color Values

Finding a color value for the object is crucial to swatch working well. This guide will
explain some tips on how to do this.

## Color Test

A good way to get started is to get an image you plan to run color tests on, crop it to 
the `zone` it will have, and then pass it to `/api/colortest`.

This will return a response like:

```json
{'message': 'The dominant color is (29, 131, 147) with a mixed palette as [(25, 124, 140), (152, 226, 232), (132, 172, 188), (60, 180, 196)]', 'success': True}
```

The response is a list of `(R, G, B)` values that represent the color of a pixel. The next step is to take these values and put them into the [Google Colorpicker](https://g.co/kgs/jXDLWb) and see which values look close to the object you are trying to detect.

Once this is done, the values need to be converted to a color variant in the config.

```yaml
color_variants:
  default:
    color_lower: 26, 118, 130
    color_upper: 34, 144, 162
```

I got these values by multiplying the closest color values (in this case the dominant color, but that won't always be true) by 90% for the color_lower and by 110% for the color_upper. This will give a decent spread and hopefully catch most values. This can then be tested and `detected` or `miss` snapshots will be saved which can then be referenced to see which parts of the object were or were not detected, and the lower and upper values can be adjusted accordingly.

NOTE: There are plans to create a UI to make this easier.

## Multiple Color Variants

It is common for objects to appear as different colors based on the sunlight and other conditions, so Swatch supports the ability to save multiple color variants for the same object so it can be detected in multiple lighting conditions. Follow the steps above with an image with those lighting conditions and add it as another `color_variant`.
