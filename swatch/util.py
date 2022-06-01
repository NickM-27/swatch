"""Utilities and convenience funs."""

from typing import Any, Dict, Set, Tuple

from colorthief import ColorThief
import cv2
import numpy as np

from swatch.config import ColorVariantConfig, ObjectConfig


def mask_image(crop: Any, color_variant: ColorVariantConfig) -> Tuple[Any, int]:
    """Mask an image with color values"""
    color_lower = (
        "1, 1, 1"
        if color_variant.color_lower == "0, 0, 0"
        else color_variant.color_lower.split(", ")
    )
    color_upper = color_variant.color_upper.split(", ")

    lower: np.ndarray = np.array(
        [int(color_lower[0]), int(color_lower[1]), int(color_lower[2])],
        dtype="uint8",
    )
    upper: np.ndarray = np.array(
        [int(color_upper[0]), int(color_upper[1]), int(color_upper[2])],
        dtype="uint8",
    )

    mask = cv2.inRange(crop, lower, upper)
    output = cv2.bitwise_and(crop, crop, mask=mask)
    matches = np.count_nonzero(output)
    return (output, matches)


def detect_objects(mask: Any, obj: ObjectConfig) -> Set[Dict[str, Any]]:
    """Detect objects and return list of bounding boxes."""
    # get gray image
    gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # calculate contours
    _, thresh = cv2.threshold(gray, 1, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = w * h

        if obj.min_area < area < obj.max_area:
            detected.append(
                {
                    "box": [x, y, x + w, y + h],
                    "area": area,
                }
            )

    return detected


def parse_colors_from_image(test_image: Any) -> tuple[str, set[str]]:
    """Convenience fun to get colors from test image."""
    color_thief = ColorThief(test_image)
    main_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=3)
    return (main_color, palette)
