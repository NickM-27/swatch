"""Handles creation and deletion of snapshots."""

import datetime
import multiprocessing
import os
import threading

import cv2
from numpy import ndarray

from swatch.config import SnapshotConfig
from swatch.const import CONST_MEDIA_DIR


def save_snapshot(name: str, image: ndarray) -> bool:
    """Saves the snapshot to the correct snapshot dir."""
    time = datetime.datetime.now()

    file_dir = f"{CONST_MEDIA_DIR}/snapshots/{time.strftime('%m-%d')}"

    if not os.path.exists(file_dir):
        print(f"{file_dir} doesn't exist, creating...")
        os.makedirs(file_dir)
        print(f"after creating {os.listdir('/media/')}")
        return False

    file = f"{file_dir}/{name}_{time.strftime('%f')}.jpg"
    cv2.imwrite(file, image)
    return True


class SnapshotCleanup(threading.Thread):
    """Cleanup snapshots so dir doesn't take up too much storage."""

    def __init__(
        self,
        snapshot_config: SnapshotConfig,
        stop_event: multiprocessing.Event,
    ):
        """Initialize snapshot cleanup."""
        threading.Thread.__init__(self)
        self.name = "snapshot_cleanup"
        self.config = snapshot_config
        self.stop_event = stop_event

    def cleanup_snapshots(self):
        "Cleanup expired snapshots."
        seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7))
        valid_month, _, valid_day = seven_days_ago.strftime("%m-%d").split("-")

        for snap_dir in os.walk(f"{CONST_MEDIA_DIR}/snapshots/"):
            # delete if older than last valid
            month, _, day = str(snap_dir).split("-")

            if month == valid_month and valid_day > day:
                file_path = f"{CONST_MEDIA_DIR}/snapshots/{month}-{day}"
                try:
                    os.remove(file_path)
                except OSError as _e:
                    print(f"Error: {file_path} : {_e.strerror}")

    def run(self):
        """Run snapshot cleanup"""
        # try to run once a day
        while not self.stop_event.wait(86400):
            print("Running snapshot cleanup")

            if self.config.retain_days > 0:
                self.cleanup_snapshots()
