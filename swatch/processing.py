"""For processing of images."""

import threading
import multiprocessing

from swatch.config import CameraConfig

class AutoDetector(threading.Thread):
    """Handles the auto running of detection on cameras."""

    def __init__(
        self,
        camera_config: CameraConfig,
        stop_event: multiprocessing.Event,
    ):
        threading.Thread.__init__(self)
        self.config = camera_config
        self.stop_event = stop_event

    def run(self):
        print("Running auto detection.")

        while not self.stop_event.wait(self.config.auto_detect):
            print("Running in the loop.")