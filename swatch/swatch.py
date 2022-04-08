import requests
import cv2
import numpy as np
import os

from config import SwatchConfig, SnapshotModeEnum
from snapshot import save_snapshot
from const import CONST_CONFIG_FILE


class SwatchService:
    def __init__(self):
        print("SwatchService Starting")
        self.init_config()

    def __check_image__(self, crop, zone, object, snapshot):
        color_lower = object.color_lower.split(", ")
        color_upper = object.color_upper.split(", ")
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

        if matches > object.min_area and matches < object.max_area:
            if snapshot[1].save_detections and snapshot[1].snapshot_mode in [
                SnapshotModeEnum.all,
                SnapshotModeEnum.mask,
            ]:
                save_snapshot(f"detected_{snapshot[0]}", output)

            return {"result": True, "area": matches}
        else:
            if snapshot[1].save_misses and snapshot[1].snapshot_mode in [
                SnapshotModeEnum.all,
                SnapshotModeEnum.mask,
            ]:
                save_snapshot(f"missed_{snapshot[0]}", output)

            return {"result": False, "area": matches}

    def detect(self, camera_name, image_url):
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
                crop = []

            if crop.size <= 0:
                continue

            for object_name in zone.objects:
                snapshot_config = zone.snapshot_config
                result = self.__check_image__(
                    crop,
                    zone,
                    self.config.objects[object_name],
                    (f"{zone_name}_{object_name}", snapshot_config),
                )

                if snapshot_config.snapshot_mode in [
                    SnapshotModeEnum.all,
                    SnapshotModeEnum.crop,
                ]:
                    save_snapshot(f"{zone_name}", crop)

                response[zone_name][object_name] = result

        return response

    def init_config(self):
        print("Importing config")

        if os.path.isfile(CONST_CONFIG_FILE):
            print("Verified")

        user_config = SwatchConfig.parse_file(CONST_CONFIG_FILE)
        self.config = user_config.runtime_config
