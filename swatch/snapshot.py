"""Handles creation and deletion of snapshots."""

import datetime
import multiprocessing
import os
import requests
import shutil
import threading
from typing import Any

import cv2
import numpy as np
from numpy import ndarray

from swatch.config import SwatchConfig, CameraConfig
from swatch.const import CONST_MEDIA_DIR


def delete_dir(date_dir: str, camera_name: str):
    """Deletes a date and camera dir"""
    file_path = f"{date_dir}/{camera_name}"

    try:
        print(f"Cleaning up {file_path}")
        shutil.rmtree(file_path)

        if len(os.listdir(date_dir)) == 0:
            os.rmdir(date_dir)
    except OSError as _e:
        print(f"Error: {file_path} : {_e.strerror}")


class SnapshotProcessor:
    """Process snapshot requests."""

    def __init__(self, config: SwatchConfig) -> None:
        self.config = config

    def save_snapshot(
        self,
        camera_name: str,
        file_name: str,
        image: ndarray,
    ) -> bool:
        """Saves the snapshot to the correct snapshot dir."""
        time = datetime.datetime.now()

        file_dir = f"{CONST_MEDIA_DIR}/snapshots/{time.strftime('%m-%d')}/{camera_name}"

        if not os.path.exists(file_dir):
            print(f"{file_dir} doesn't exist, creating...")
            os.makedirs(file_dir)
            print(f"after creating {os.listdir('/media/')}")
            return False

        file = f"{file_dir}/{file_name}_{time.strftime('%f')}.jpg"
        cv2.imwrite(file, image)
        return True

    def get_latest_camera_snapshot(
        self,
        camera_name: str,
    ) -> Any:
        """Get the latest snapshot for <camera_name> and <zone_name>."""
        imgBytes = requests.get(
            self.config.cameras[camera_name].snapshot_config.url
        ).content

        if not imgBytes:
            return None

        img = cv2.imdecode(np.asarray(bytearray(imgBytes), dtype=np.uint8), -1)
        ret, jpg = cv2.imencode(".jpg", img, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return jpg.tobytes()

    def get_latest_zone_snapshot(
        self,
        camera_name: str,
        zone_name: str,
    ) -> Any:
        """Get the latest snapshot for <camera_name>."""
        camera_config: CameraConfig = self.config.cameras[camera_name]
        imgBytes = requests.get(camera_config.snapshot_config.url).content

        if not imgBytes:
            return None

        img = cv2.imdecode(np.asarray(bytearray(imgBytes), dtype=np.uint8), -1)
        coordinates = camera_config.zones[zone_name].coordinates.split(", ")
        crop = img[
            int(coordinates[1]) : int(coordinates[3]),
            int(coordinates[0]) : int(coordinates[2]),
        ]

        ret, jpg = cv2.imencode(".jpg", crop, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        return jpg.tobytes()

    def get_latest_detection(self, camera_name: str) -> Any:
        """Get the latest detection for a <camera_name>."""
        snaps_dir = f"{CONST_MEDIA_DIR}/snapshots"
        print(f"snaps dir is {snaps_dir}")
        recent_folder = max(
            [os.path.join(snaps_dir, basename) for basename in os.listdir(snaps_dir)]
        )
        print(f"")

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
        camera_config: CameraConfig,
        stop_event: multiprocessing.Event,
    ):
        """Initialize snapshot cleanup."""
        threading.Thread.__init__(self)
        self.name = "snapshot_cleanup"
        self.config = camera_config
        self.stop_event = stop_event

    def cleanup_snapshots(self):
        """Cleanup expired snapshots."""
        seven_days_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        valid_month, _, valid_day = seven_days_ago.strftime("%m-%d").partition("-")

        for snap_dir in os.listdir(f"{CONST_MEDIA_DIR}/snapshots/"):
            if not os.path.isdir(
                os.path.join(f"{CONST_MEDIA_DIR}/snapshots/", snap_dir)
            ):
                continue

            # delete if older than last valid
            month, _, day = str(snap_dir).partition("-")

            if month == valid_month and valid_day >= day:
                delete_dir(
                    f"{CONST_MEDIA_DIR}/snapshots/{month}-{day}", self.config.name
                )
            elif valid_month > month and (int(day) - int(valid_day)) <= 24:
                delete_dir(
                    f"{CONST_MEDIA_DIR}/snapshots/{month}-{day}", self.config.name
                )

    def run(self):
        """Run snapshot cleanup"""
        print(f"Starting snapshot cleanup for {self.config.name}")
        # try to run once a day
        while not self.stop_event.wait(86400):
            if self.config.snapshot_config.retain_days > 0:
                self.cleanup_snapshots()

        print(f"Stopping Snapshot Cleanup for {self.config.name}")
