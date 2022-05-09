""""""
import os

from swatch.config import SwatchConfig, SnapshotModeEnum
from swatch.const import CONST_CONFIG_FILE
from swatch.http import create_app
from swatch.image import ImageProcessor

class SwatchApp:

    def __init__(self):
        print("SwatchApp Starting")
        self.__init_config__()
        self.image_processor = ImageProcessor(self.config)
        self.http = create_app(
            self.config,
            self.image_processor,
        )

    def __init_config__(self):
        """Init the SwatchService with saved config file."""
        print("Importing config")

        if os.path.isfile(CONST_CONFIG_FILE):
            print("Verified Config")

        user_config = SwatchConfig.parse_file(CONST_CONFIG_FILE)
        self.config = user_config.runtime_config

    def start(self):
        """Start SwatchApp."""
        try:
            self.http.run(host="127.0.0.1", port=4500, debug=False)
        except KeyboardInterrupt:
            pass

        self.stop()

    def stop(self):
        """Stop SwatchApp."""
        print("SwatchApp Stopping")