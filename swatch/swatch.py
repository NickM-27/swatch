import os

from config import SwatchConfig, SnapshotModeEnum
from const import CONST_CONFIG_FILE
from image import ImageProcessor


class SwatchService:
    def __init__(self):
        """Init SwatchService."""
        print("SwatchService Starting")
        self.init_config()
        self.image_processor = ImageProcessor(self.config)

    def init_config(self):
        """Init the SwatchService with saved config file."""
        print("Importing config")

        if os.path.isfile(CONST_CONFIG_FILE):
            print("Verified Config")

        user_config = SwatchConfig.parse_file(CONST_CONFIG_FILE)
        self.config = user_config.runtime_config
