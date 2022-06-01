"""ImageProcessor for getting detectable info from images."""

import datetime
import logging
from typing import Any, Dict, Optional
import cv2
import numpy as np

import requests

from swatch.color import detect_objects, mask_image
from swatch.config import ObjectConfig, SnapshotModeEnum, SwatchConfig
from swatch.snapshot import SnapshotProcessor


logger = logging.getLogger(__name__)


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
        obj_config: ObjectConfig,
    ) -> Dict[str, Any]:
        """Check specific image for known color values."""
        snapshot_config = self.config.cameras[camera_name].snapshot_config
        best_fail: Dict[str, Any] = {}

        for variant_name, color_variant in obj_config.color_variants.items():
            now_time = datetime.datetime.now().strftime("%H:%M")

            if (
                now_time < color_variant.time_range.after
                or now_time > color_variant.time_range.before
            ):
                continue

            mask, matches = mask_image(crop, color_variant)
            detected_objects = detect_objects(mask, obj_config)

            if detected_objects:
                # draw bounding boxes on image if enabled
                if snapshot_config.bounding_box:
                    for obj in detected_objects:
                        cv2.rectangle(
                            crop,
                            (obj["box"][0], obj["box"][1]),
                            (obj["box"][2], obj["box"][3]),
                            (0, 255, 0),
                            2,
                        )
                        cv2.rectangle(
                            mask,
                            (obj["box"][0], obj["box"][1]),
                            (obj["box"][2], obj["box"][3]),
                            (0, 255, 0),
                            2,
                        )

                # save the snapshot if enabled
                if snapshot_config.save_detections and snapshot_config.mode in [
                    SnapshotModeEnum.ALL,
                    SnapshotModeEnum.MASK,
                ]:
                    self.snapshot_processor.save_snapshot(
                        camera_name,
                        "",
                        f"detected_{variant_name}_{file_name}_{datetime.datetime.now().strftime('%f')}.jpg",
                        mask,
                    )

                return {
                    "result": True,
                    "variant": variant_name,
                    "camera_name": camera_name,
                    "objects": detected_objects,
                }

            if matches > best_fail.get("area", 0):
                best_fail = {
                    "result": False,
                    "area": matches,
                    "variant": variant_name,
                    "camera_name": camera_name,
                }

            if snapshot_config.save_misses and snapshot_config.mode in [
                SnapshotModeEnum.ALL,
                SnapshotModeEnum.MASK,
            ]:
                self.snapshot_processor.save_snapshot(
                    camera_name,
                    "",
                    f"missed_{variant_name}_{file_name}_{datetime.datetime.now().strftime('%f')}.jpg",
                    mask,
                )

        return best_fail

    def detect(self, camera_name: str, image_url: str) -> Dict[str, Any]:
        """Use the default image or $image_url to detect known objects."""
        response: Dict[str, Any] = {}

        camera_config = self.config.cameras[camera_name]

        for zone_name, zone in camera_config.zones.items():
            response[zone_name] = {}
            img_bytes = requests.get(image_url).content

            if img_bytes is None:
                continue

            img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), -1)

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
                )

                if snapshot_config.mode in [
                    SnapshotModeEnum.ALL,
                    SnapshotModeEnum.CROP,
                ]:
                    self.snapshot_processor.save_snapshot(
                        camera_name,
                        zone_name,
                        f"{zone_name}_{datetime.datetime.now().strftime('%f')}.jpg",
                        crop,
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
        _, jpg = cv2.imencode(".jpg", output, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return jpg.tobytes()
