"""For processing of images."""

import datetime
import logging
import multiprocessing
import random
import string
import threading
from typing import Any, Dict

from swatch.config import CameraConfig, SwatchConfig
from swatch.image import ImageProcessor
from swatch.models import Detection
from swatch.snapshot import SnapshotProcessor


class AutoDetector(threading.Thread):
    """Handles the auto running of detection on cameras."""

    def __init__(
        self,
        image_processor: ImageProcessor,
        snap_processor: SnapshotProcessor,
        camera_config: CameraConfig,
        stop_event: multiprocessing.Event,
    ) -> None:
        threading.Thread.__init__(self)
        self.image_processor = image_processor
        self.snap_processor = snap_processor
        self.config = camera_config
        self.stop_event = stop_event
        self.obj_data: Dict[str, Any] = {}

    def __handle_db__(self, db_type: str, obj_id: str) -> None:
        """Handle the db transactions for detection."""
        now = datetime.datetime.now().timestamp()

        if db_type == "new":
            Detection.insert(
                id=self.obj_data[obj_id]["id"],
                label=self.obj_data[obj_id]["object_name"],
                camera=self.config.name,
                zone=self.obj_data[obj_id]["zone_name"],
                color_variant=self.obj_data[obj_id]["variant"],
                start_time=now,
                top_area=self.obj_data[obj_id]["top_area"],
            ).execute()
        elif db_type == "update":
            Detection.update(
                color_variant=self.obj_data[obj_id]["variant"],
                top_area=self.obj_data[obj_id]["top_area"],
            ).where(Detection.id == self.obj_data[obj_id]["id"]).execute()
        elif db_type == "end":
            Detection.update(
                color_variant=self.obj_data[obj_id]["variant"],
                top_area=self.obj_data[obj_id]["top_area"],
                end_time=now,
            ).where(Detection.id == self.obj_data[obj_id]["id"]).execute()

    def __handle_detections__(self, detection_result: Dict[str, Any]) -> None:
        """Run through map of detections for camera and add to the db."""
        cam_name = self.config.name

        for zone_name, objects in detection_result.items():
            for object_name, object_result in objects.items():
                non_unique_id = f"{cam_name}.{zone_name}.{object_name}"

                if not self.obj_data.get(non_unique_id) and not object_result.get(
                    "result"
                ):
                    continue

                if not self.obj_data.get(non_unique_id):
                    self.obj_data[non_unique_id] = {}

                unique_id = (
                    f"{non_unique_id}.{''.join(random.choices(string.ascii_lowercase + string.digits, k=6))}"
                    if not self.obj_data[non_unique_id].get("id")
                    else self.obj_data[non_unique_id]["id"]
                )

                self.obj_data[non_unique_id]["object_name"] = object_name
                self.obj_data[non_unique_id]["zone_name"] = zone_name
                self.obj_data[non_unique_id]["variant"] = object_result["variant"]

                top_area = max([d["area"] for d in object_result["objects"]])

                if top_area > self.obj_data[non_unique_id].get("top_area", 0):
                    self.obj_data[non_unique_id]["top_area"] = top_area

                    # save snapshot with best area
                    self.snap_processor.save_snapshot(
                        cam_name,
                        zone_name,
                        f"{unique_id}.jpg",
                        None,
                    )

                if not self.obj_data[non_unique_id].get("id"):
                    self.obj_data[non_unique_id]["id"] = unique_id
                    self.__handle_db__("new", non_unique_id)
                else:
                    if object_result["result"]:
                        self.__handle_db__("update", non_unique_id)
                    else:
                        self.__handle_db__("end", non_unique_id)
                        del self.obj_data[non_unique_id]

    def run(self) -> None:
        logging.info(f"Starting Auto Detection for {self.config.name}")

        while not self.stop_event.wait(self.config.auto_detect):
            result: Dict[str, Any] = self.image_processor.detect(
                self.config.name, self.config.snapshot_config.url
            )
            self.__handle_detections__(result)

        # ensure db doesn't contain bad data after shutdown
        Detection.update(end_time=datetime.datetime.now().timestamp()).where(
            Detection.end_time is None
        ).execute()
        logging.info(f"Stopping Auto Detection for {self.config.name}")


class DetectionCleanup(threading.Thread):
    """Handles the auto cleanup of detections."""

    def __init__(self, config: SwatchConfig, stop_event: multiprocessing.Event):
        threading.Thread.__init__(self)
        self.config: SwatchConfig = config
        self.stop_event: multiprocessing.Event = stop_event

    def __cleanup_db__(self):
        """Cleanup the old events in the db."""

        for cam_name, cam_config in self.config.cameras.items():
            expire_days = cam_config.snapshot_config.retain_days
            expire_after = (
                datetime.datetime.now() - datetime.timedelta(days=expire_days)
            ).timestamp()

            Detection.delete().where(
                Detection.camera == cam_name,
                Detection.start_time < expire_after,
            )

    def run(self) -> None:
        logging.info("Starting Detection Cleanup")

        while not self.stop_event.wait(3600):
            self.__cleanup_db__()

        logging.info("Stopping Detection Cleanup")
