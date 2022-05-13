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
        camera_config: CameraConfig,
        stop_event: multiprocessing.Event,
    ):
        threading.Thread.__init__(self)
        self.image_processor = image_processor
        self.config = camera_config
        self.stop_event = stop_event

    def run(self):
        print(f"Starting Auto Detection for {self.config.name}")

        while not self.stop_event.wait(self.config.auto_detect):
            self.image_processor(self.config.name, None)

        print(f"Stopping Auto Detection for {self.config.name}")