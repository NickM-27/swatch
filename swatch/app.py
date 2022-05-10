"""Main SwatchApp responsible for running the app."""
import os

from waitress import serve

from swatch.config import SwatchConfig, SnapshotModeEnum
from swatch.const import CONST_CONFIG_FILE
from swatch.http import create_app
from swatch.image import ImageProcessor


class SwatchApp:
    def __init__(self) -> None:
        print("SwatchApp Starting")
        self.__init_config__()
        self.image_processor = ImageProcessor(self.config)
        self.http = create_app(
            self.config,
            self.image_processor,
        )

    def __init_config__(self) -> None:
        """Init the SwatchService with saved config file."""
        print("Importing config")

        if os.path.isfile(CONST_CONFIG_FILE):
            print("Verified Config")

        user_config = SwatchConfig.parse_file(CONST_CONFIG_FILE)
        self.config = user_config.runtime_config

    def start(self) -> None:
        """Start SwatchApp."""
        try:
            serve(self.http, listen="*:4500")
        except KeyboardInterrupt:
            pass

        self.stop()

    def stop(self) -> None:
        """Stop SwatchApp."""
        print("SwatchApp Stopping")
