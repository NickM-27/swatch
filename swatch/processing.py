"""For processing of images."""

import threading
import multiprocessing

from swatch.config import CameraConfig
from swatch.image import ImageProcessor

class AutoDetector(threading.Thread):
    """Handles the auto running of detection on cameras."""

    def __init__(
        self,
        image_processor: ImageProcessor,
        camera_name: str,
        camera_config: CameraConfig,
        stop_event: multiprocessing.Event,
    ):
        threading.Thread.__init__(self)
        self.image_processor = image_processor
        self.camera_name = camera_name
        self.config = camera_config
        self.stop_event = stop_event

    def run(self):
        print(f"Running auto detection for {self.camera_name}.")

        while not self.stop_event.wait(self.config.auto_detect):
            self.image_processor(self.camera_name, None)