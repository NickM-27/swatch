"""Main SwatchApp responsible for running the app."""
import os
import multiprocessing

from waitress import serve

from swatch.config import SwatchConfig, SnapshotModeEnum
from swatch.const import CONST_CONFIG_FILE
from swatch.http import create_app
from swatch.image import ImageProcessor


class SwatchApp:
    """Main swatch process that handles the lifecycle of the app."""

    def __init__(self) -> None:
        print("SwatchApp Starting")
        self.__init_config__()
        self.image_processor = ImageProcessor(self.config)
        self.http = create_app(
            self.config,
            self.image_processor,
        )
        self.stop_event = multiprocessing.Event()

    def __init_config__(self) -> None:
        """Init the SwatchService with saved config file."""
        print("Importing SwatchApp Config")

        config_file = os.environ.get("CONFIG_FILE", CONST_CONFIG_FILE)

        if os.path.isfile(config_file):
            print("Verified SwatchApp Config")

        user_config = SwatchConfig.parse_file(config_file)
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
        self.stop_event.set()
