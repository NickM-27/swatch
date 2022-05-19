"""For processing of images."""

import datetime
import multiprocessing
import random
import string
import threading
from typing import Any, Dict

from swatch.config import CameraConfig
from swatch.image import ImageProcessor
from swatch.models import Detection


class AutoDetector(threading.Thread):
    """Handles the auto running of detection on cameras."""

    def __init__(
        self,
        image_processor: ImageProcessor,
        camera_config: CameraConfig,
        stop_event: multiprocessing.Event,
    ) -> None:
        threading.Thread.__init__(self)
        self.image_processor = image_processor
        self.config = camera_config
        self.stop_event = stop_event
        self.obj_data: Dict[str, Any] = {}

    def __handle_db__(self, db_type: str, obj_id: str) -> None:
        """Handle the db transactions for detection."""
        if db_type == "new":
            Detection.insert(
                id = self.obj_data[obj_id]["id"],
                label = self.obj_data[obj_id]["object_name"],
                camera = self.config.name,
                zone = self.obj_data[obj_id]["zone_name"],
                color_variant = self.obj_data[obj_id]["variant"],
                start_time = datetime.datetime().timestamp(),
                top_area = self.obj_data[obj_id]["top_area"],
            )
        elif db_type == "update":
            Detection.update(

            ).where(Detection.id == self.obj_data[obj_id]["id"])
        elif db_type == "end":
            Detection.update(

            ).where(Detection.id == self.obj_data[obj_id]["id"])

    def __handle_detections__(self, detection_result: Dict[str, Any]) -> None:
        """Run through map of detections for camera and add to the db."""
        cam_name = self.config.name

        for zone_name, objects in detection_result.items():
            for object_name, object_result in objects.items():
                non_unique_id = f"{cam_name}.{zone_name}.{object_name}"

                if not self.obj_data[non_unique_id] and not object_result["result"]:
                    continue

                self.obj_data[non_unique_id]["object_name"] = object_name
                self.obj_data[non_unique_id]["zone_name"] = zone_name
                self.obj_data[non_unique_id]["variant"] = object_result["variant"]

                if object_result["area"] > self.obj_data[non_unique_id].get("top_area", 0):
                    self.obj_data[non_unique_id]["top_area"] = object_result["area"]

                if not self.obj_data[non_unique_id]:
                    unique_id = f"{non_unique_id}.{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
                    self.obj_data[non_unique_id]["id"] = unique_id
                    self.__handle_db__("new", non_unique_id)
                else:
                    if object_result["result"]:
                        self.__handle_db__("update", non_unique_id)
                    else:
                        self.__handle_db__("end", non_unique_id)
                        del self.obj_data[non_unique_id]


    def run(self) -> None:
        print(f"Starting Auto Detection for {self.config.name}")

        while not self.stop_event.wait(self.config.auto_detect):
            result: Dict[str, Any] = self.image_processor.detect(
                self.config.name, self.config.snapshot_config.url
            )
            self.__handle_detections__(result)

        print(f"Stopping Auto Detection for {self.config.name}")
