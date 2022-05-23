"""ImageProcessor for getting detectable info from images."""

import datetime
from typing import Any, Dict, Optional, Tuple
from colorthief import ColorThief
import cv2
import numpy as np

import requests

from swatch.config import (
    ColorVariantConfig,
    ObjectConfig,
    SnapshotConfig,
    SnapshotModeEnum,
    SwatchConfig,
)
from swatch.snapshot import SnapshotProcessor


def __mask_image__(crop: Any, color_variant: ColorVariantConfig) -> Tuple[Any, int]:
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


class ImageProcessor:
    """Processing images with swatch config data."""

    def __init__(
        self,
        config: SwatchConfig,
        snapshot_processor: SnapshotProcessor,
    ) -> None:
        """Create Image Processor"""
        self.config: SwatchConfig = config
        self.snapshot_processor: SnapshotProcessor = snapshot_processor
        self.latest_results: Dict[str, Any] = {}

    def __check_image__(
        self,
        crop: Any,
        camera_name: str,
        file_name: str,
        detectable: ObjectConfig,
        snapshot: SnapshotConfig,
    ) -> Dict[str, Any]:
        """Check specific image for known color values."""
        best_fail: Dict[str, Any] = {}

        for variant_name, color_variant in detectable.color_variants.items():
            now_time = datetime.datetime.now().strftime("%H:%M")

            if (
                now_time < color_variant.time_range.after
                or now_time > color_variant.time_range.before
            ):
                continue

            output, matches = __mask_image__(crop, color_variant)

            if matches > detectable.min_area and matches < detectable.max_area:
                if snapshot.save_detections and snapshot.mode in [
                    SnapshotModeEnum.ALL,
                    SnapshotModeEnum.MASK,
                ]:
                    self.snapshot_processor.save_snapshot(
                        camera_name, f"detected_{variant_name}_{file_name}", output
                    )

                return {
                    "result": True,
                    "area": matches,
                    "variant": variant_name,
                    "camera_name": camera_name,
                }
            else:
                if matches > best_fail.get("area", 0):
                    best_fail = {
                        "result": False,
                        "area": matches,
                        "variant": variant_name,
                        "camera_name": camera_name,
                    }

                if snapshot.save_misses and snapshot.mode in [
                    SnapshotModeEnum.ALL,
                    SnapshotModeEnum.MASK,
                ]:
                    self.snapshot_processor.save_snapshot(
                        camera_name, f"missed_{variant_name}_{file_name}", output
                    )

        return best_fail

    def detect(self, camera_name: str, image_url: str) -> Dict[str, Any]:
        """Use the default image or $image_url to detect known objects."""
        response: Dict[str, Any] = {}

        camera_config = self.config.cameras[camera_name]

        for zone_name, zone in camera_config.zones.items():
            response[zone_name] = {}
            imgBytes = requests.get(image_url).content

            if not imgBytes:
                continue

            img = cv2.imdecode(np.asarray(bytearray(imgBytes), dtype=np.uint8), -1)

            coordinates = zone.coordinates.split(", ")

            if img.size > 0:
                crop = img[
                    int(coordinates[1]) : int(coordinates[3]),
                    int(coordinates[0]) : int(coordinates[2]),
                ]
            else:
                continue

            for object_name in zone.objects:
                snapshot_config = camera_config.snapshot_config
                result = self.__check_image__(
                    crop,
                    camera_name,
                    f"{zone_name}_{object_name}",
                    self.config.objects[object_name],
                    snapshot_config,
                )

                if snapshot_config.mode in [
                    SnapshotModeEnum.ALL,
                    SnapshotModeEnum.CROP,
                ]:
                    self.snapshot_processor.save_snapshot(
                        camera_name, f"{zone_name}", crop
                    )

                self.latest_results[object_name] = result
                response[zone_name][object_name] = result

        return response

    def get_latest_result(self, label: str) -> Dict[str, Any]:
        """Return latest results for label."""
        if label == "all":
            return self.latest_results

        latest_result: Optional[Dict[str, Any]] = self.latest_results.get(label)

        if latest_result:
            return latest_result

        return {"result": False, "area": -1}

    def parse_colors_from_image(self, test_image: Any) -> tuple[str, set[str]]:
        """Convenience fun to get colors from test image."""
        color_thief = ColorThief(test_image)
        main_color = color_thief.get_color(quality=1)
        palette = color_thief.get_palette(color_count=3)
        return (main_color, palette)

    def mask_test_image(self, img_str: str, color_lower: str, color_upper: str) -> Any:
        """Mask a test image with provided color range."""
        img = cv2.imdecode(np.fromstring(img_str, np.uint8), -1)

        if color_lower == "0, 0, 0":
            color_lower = ["1", "1", "1"]
        else:
            color_lower = color_lower.split(", ")

        color_upper = color_upper.split(", ")
        lower: np.ndarray = np.array(
            [int(color_lower[0]), int(color_lower[1]), int(color_lower[2])],
            dtype="uint8",
        )
        upper: np.ndarray = np.array(
            [int(color_upper[0]), int(color_upper[1]), int(color_upper[2])],
            dtype="uint8",
        )

        mask = cv2.inRange(img, lower, upper)
        output = cv2.bitwise_and(img, img, mask=mask)
        ret, jpg = cv2.imencode(".jpg", output, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return jpg.tobytes()
