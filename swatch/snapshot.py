"""Handles creation and deletion of snapshots."""

import datetime
import multiprocessing
import os
import shutil
import threading

import cv2
from numpy import ndarray

from swatch.config import CameraConfig
from swatch.const import CONST_MEDIA_DIR


def save_snapshot(
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
