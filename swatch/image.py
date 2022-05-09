"""ImageProcessor for getting detectable info from images."""
import requests
from colorthief import ColorThief
import cv2
import numpy as np

from swatch.config import SnapshotModeEnum
from swatch.snapshot import save_snapshot


class ImageProcessor:
    """Processing images with swatch config data."""

    def __init__(self, config):
        """Create Image Processor"""
        self.config = config
        self.latest_results = {}

    def __check_image__(self, crop, detectable, snapshot):
        """Check specific image for known color values."""

        if detectable.color_lower == "0, 0, 0":
            color_lower = "1, 1, 1"
        else:
            color_lower = detectable.color_lower.split(", ")

        color_upper = detectable.color_upper.split(", ")
        lower = np.array(
            [int(color_lower[0]), int(color_lower[1]), int(color_lower[2])],
            dtype="uint8",
        )
        upper = np.array(
            [int(color_upper[0]), int(color_upper[1]), int(color_upper[2])],
            dtype="uint8",
        )

        mask = cv2.inRange(crop, lower, upper)
        output = cv2.bitwise_and(crop, crop, mask=mask)
        matches = np.count_nonzero(output)

        if matches > detectable.min_area and matches < detectable.max_area:
            if snapshot[1].save_detections and snapshot[1].snapshot_mode in [
                SnapshotModeEnum.all,
                SnapshotModeEnum.mask,
            ]:
                save_snapshot(f"detected_{snapshot[0]}", output)

            return {"result": True, "area": matches}

        if snapshot[1].save_misses and snapshot[1].snapshot_mode in [
            SnapshotModeEnum.all,
            SnapshotModeEnum.mask,
        ]:
            save_snapshot(f"missed_{snapshot[0]}", output)

        return {"result": False, "area": matches}

    def detect(self, camera_name: str, image_url: str):
        """Use the default image or $image_url to detect known objects."""
        response = {}

        for zone_name, zone in self.config.cameras[camera_name].zones.items():
            response[zone_name] = {}
            imgBytes = requests.get(image_url).content
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
                snapshot_config = zone.snapshot_config
                result = self.__check_image__(
                    crop,
                    self.config.objects[object_name],
                    (f"{zone_name}_{object_name}", snapshot_config),
                )

                if snapshot_config.snapshot_mode in [
                    SnapshotModeEnum.all,
                    SnapshotModeEnum.crop,
                ]:
                    save_snapshot(f"{zone_name}", crop)

                self.latest_results[object_name] = result
                response[zone_name][object_name] = result

        return response

    def get_latest_result(self, label: str):
        """Return latest results for label."""
        if label == "all":
            return self.latest_results

        latest_result = self.latest_results.get(label)

        if latest_result:
            return latest_result

        return {"result": False, "area": -1}

    def parse_colors_from_image(self, test_image) -> tuple[str, set[str]]:
        """Convenience fun to get colors from test image."""
        color_thief = ColorThief(test_image)
        main_color = color_thief.get_color(quality=1)
        palette = color_thief.get_palette(color_count=3)
        return (main_color, palette)
