"""Handles creation and deletion of snapshots."""

import datetime
import logging
import multiprocessing
import os
import requests
import shutil
import threading
from typing import Any, Set

import cv2
import numpy as np
from numpy import ndarray

from swatch.config import SwatchConfig, CameraConfig
from swatch.const import CONST_MEDIA_DIR
from swatch.models import Detection


logger = logging.getLogger(__name__)


def delete_dir(date_dir: str, camera_name: str):
    """Deletes a date and camera dir"""
    file_path = f"{date_dir}/{camera_name}"

    try:
        logger.debug("Cleaning up %s", file_path)
        shutil.rmtree(file_path)

        if len(os.listdir(date_dir)) == 0:
            os.rmdir(date_dir)
    except OSError as _e:
        logger.error("Error: %s : %s", file_path, _e.strerror)


class SnapshotProcessor:
    """Process snapshot requests."""

    def __init__(self, config: SwatchConfig) -> None:
        self.config = config
        self.media_dir = os.environ.get("MEDIA_DIR", CONST_MEDIA_DIR)

    def save_snapshot(
        self,
        camera_name: str,
        zone_name: str,
        file_name: str,
        image: ndarray,
    ) -> bool:
        """Saves the file snapshot to the correct snapshot dir."""
        time = datetime.datetime.now()

        file_dir = f"{self.media_dir}/snapshots/{time.strftime('%m-%d')}/{camera_name}"

        if not os.path.exists(file_dir):
            logger.debug("%s doesn't exist, creating...", file_dir)
            os.makedirs(file_dir)

        file = f"{file_dir}/{file_name}"

        if image is not None:
            cv2.imwrite(file, image)
        else:
            try:
                img_bytes = requests.get(
                    self.config.cameras[camera_name].snapshot_config.url
                ).content
            except ConnectionError:
                img_bytes = None

            if img_bytes is None:
                return False

            img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), -1)

            coordinates = (
                self.config.cameras[camera_name]
                .zones[zone_name]
                .coordinates.split(", ")
            )

            if img.size > 0:
                crop = img[
                    int(coordinates[1]) : int(coordinates[3]),
                    int(coordinates[0]) : int(coordinates[2]),
                ]

            cv2.imwrite(file, crop)

        return True

    def save_detection_snapshot(
        self,
        camera_name: str,
        zone_name: str,
        detection_id: str,
        bounding_box: Set[int],
    ) -> bool:
        """Saves the file snapshot for a detection to the correct snapshot dir."""
        time = datetime.datetime.now()

        file_dir = f"{self.media_dir}/snapshots/{time.strftime('%m-%d')}/{camera_name}"

        if not os.path.exists(file_dir):
            logger.debug("%s doesn't exist, creating...", file_dir)
            os.makedirs(file_dir)

        try:
            img_bytes = requests.get(
                self.config.cameras[camera_name].snapshot_config.url
            ).content
        except ConnectionError:
            img_bytes = None


        if img_bytes is None:
            return False

        img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), -1)

        crop_cords = (
            self.config.cameras[camera_name].zones[zone_name].coordinates.split(", ")
        )

        if img.size > 0:
            crop = img[
                int(crop_cords[1]) : int(crop_cords[3]),
                int(crop_cords[0]) : int(crop_cords[2]),
            ]

        snapshot_config = self.config.cameras[camera_name].snapshot_config

        if snapshot_config.clean_snapshot:
            cv2.imwrite(f"{file_dir}/{detection_id}-clean.png", crop)

        if snapshot_config.bounding_box:
            cv2.rectangle(
                crop,
                (bounding_box[0], bounding_box[1]),
                (bounding_box[2], bounding_box[3]),
                (0, 255, 0),
                2,
            )

        cv2.imwrite(f"{file_dir}/{detection_id}.jpg", crop)
        return True

    def get_detection_snapshot(self, detection: Detection) -> Any:
        """Get file snapshot for a specific detection."""
        file_dir = f"{self.media_dir}/snapshots/{datetime.datetime.fromtimestamp(detection.start_time).strftime('%m-%d')}/{detection.camera}"

        if not os.path.exists(file_dir) and detection.end_time:
            file_dir = f"{self.media_dir}/snapshots/{datetime.datetime.fromtimestamp(detection.end_time).strftime('%m-%d')}/{detection.camera}"

        if not os.path.exists(file_dir):
            return None

        file = f"{file_dir}/{detection.id}.jpg"

        try:
            with open(file, "rb") as image_file:
                jpg_bytes = image_file.read()

            return jpg_bytes
        except Exception:
            return None

    def get_latest_camera_snapshot(
        self,
        camera_name: str,
    ) -> Any:
        """Get the latest web snapshot for <camera_name> and <zone_name>."""
        try:
            img_bytes = requests.get(
                self.config.cameras[camera_name].snapshot_config.url
            ).content
        except ConnectionError:
            img_bytes = None

        if img_bytes is None:
            return None

        img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), -1)
        _, jpg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return jpg.tobytes()

    def get_latest_zone_snapshot(
        self,
        camera_name: str,
        zone_name: str,
    ) -> Any:
        """Get the latest web snapshot for <camera_name>."""
        camera_config: CameraConfig = self.config.cameras[camera_name]

        try:
            img_bytes = requests.get(camera_config.snapshot_config.url).content
        except ConnectionError:
            img_bytes = None

        if not img_bytes:
            return None

        img = cv2.imdecode(np.asarray(bytearray(img_bytes), dtype=np.uint8), -1)
        coordinates = camera_config.zones[zone_name].coordinates.split(", ")
        crop = img[
            int(coordinates[1]) : int(coordinates[3]),
            int(coordinates[0]) : int(coordinates[2]),
        ]

        ret, jpg = cv2.imencode(".jpg", crop, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return jpg.tobytes()

    def get_latest_detection_snapshot(self, camera_name: str) -> Any:
        """Get the latest file snapshot for a <camera_name> detection."""
        snaps_dir = f"{self.media_dir}/snapshots"
        recent_folder = max(
            [os.path.join(snaps_dir, basename) for basename in os.listdir(snaps_dir)]
        )

        cam_snaps_dir = f"{recent_folder}/{camera_name}"
        recent_snap = max(
            [
                os.path.join(cam_snaps_dir, basename)
                for basename in os.listdir(cam_snaps_dir)
            ]
        )

        with open(recent_snap) as image_file:
            jpg_bytes = image_file.read()

        return jpg_bytes


class SnapshotCleanup(threading.Thread):
    """Cleanup snapshots so dir doesn't take up too much storage."""

    def __init__(
        self,
        config: SwatchConfig,
        stop_event: multiprocessing.Event,
    ):
        """Initialize snapshot cleanup."""
        threading.Thread.__init__(self)
        self.name = "snapshot_cleanup"
        self.config = config
        self.media_dir = os.environ.get("MEDIA_DIR", CONST_MEDIA_DIR)
        self.stop_event = stop_event

    def cleanup_snapshots(self, camera_config: CameraConfig):
        """Cleanup expired snapshots."""
        retain_days_ago = datetime.datetime.now() - datetime.timedelta(
            days=camera_config.snapshot_config.retain_days
        )
        valid_month, _, valid_day = retain_days_ago.strftime("%m-%d").partition("-")

        for snap_dir in os.listdir(f"{self.media_dir}/snapshots/"):
            if not os.path.isdir(
                os.path.join(f"{self.media_dir}/snapshots/", snap_dir)
            ):
                continue

            # delete if older than last valid
            month, _, day = str(snap_dir).partition("-")

            if month == valid_month and valid_day >= day:
                delete_dir(
                    f"{self.media_dir}/snapshots/{month}-{day}", camera_config.name
                )
            elif valid_month > month and (int(day) - int(valid_day)) <= 24:
                delete_dir(
                    f"{self.media_dir}/snapshots/{month}-{day}", camera_config.name
                )

    def run(self):
        """Run snapshot cleanup"""
        logger.info("Starting snapshot cleanup")

        # try to run once a day
        while not self.stop_event.wait(86400):

            for _, cam_config in self.config.cameras.items():
                if cam_config.snapshot_config.retain_days > 0:
                    self.cleanup_snapshots(cam_config)

        logger.info("Stopping Snapshot Cleanup")
