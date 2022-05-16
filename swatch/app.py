"""Main SwatchApp responsible for running the app."""
import os
import multiprocessing
from typing import Dict

from swatch.config import SwatchConfig
from swatch.const import CONST_CONFIG_FILE
from swatch.http import create_app
from swatch.image import ImageProcessor
from swatch.processing import AutoDetector
from swatch.snapshot import SnapshotCleanup, SnapshotProcessor


class SwatchApp:
    """Main swatch process that handles the lifecycle of the app."""

    def __init__(self) -> None:
        """Init SwatchApp."""
        print("Starting SwatchApp")
        self.stop_event = multiprocessing.Event()
        self.__init_config__()
        self.__init_processing__()
        self.__init_snapshot_cleanup__()
        self.__init_web_server__()

    def __init_config__(self) -> None:
        """Init SwatchApp with saved config file."""
        print("Importing SwatchApp Config")

        config_file = os.environ.get("CONFIG_FILE", CONST_CONFIG_FILE)

        if os.path.isfile(config_file):
            print("Verified SwatchApp Config")

        user_config = SwatchConfig.parse_file(config_file)
        self.config = user_config.runtime_config

    def __init_processing__(self) -> None:
        """Init the SwatchApp processing thread."""
        self.snapshot_processor = SnapshotProcessor(self.config)
        self.image_processor = ImageProcessor(self.config, self.snapshot_processor)

        self.camera_processes: Dict[str, AutoDetector] = {}

        for name, config in self.config.cameras.items():
            if config.auto_detect > 0 and config.snapshot_config.url:
                self.camera_processes[name] = AutoDetector(
                    self.image_processor,
                    config,
                    self.stop_event,
                )
                self.camera_processes[name].start()

    def __init_snapshot_cleanup__(self) -> None:
        """Init the SwatchApp cleanup thread."""
        self.cleanup_processes: Dict[str, AutoDetector] = {}

        for name, config in self.config.cameras.items():
            if config.snapshot_config.retain_days > 0:
                self.cleanup_processes[name] = SnapshotCleanup(
                    config,
                    self.stop_event,
                )
                self.cleanup_processes[name].start()

    def __init_web_server__(self) -> None:
        """Init the SwatchApp web server."""
        self.http = create_app(
            self.config, self.image_processor, self.snapshot_processor
        )

    def start(self) -> None:
        """Start SwatchApp."""
        try:
            self.http.run(host="127.0.0.1", port=4501, debug=False)
        except KeyboardInterrupt:
            pass

        self.stop()

    def stop(self) -> None:
        """Stop SwatchApp."""
        print("SwatchApp Stopping")
        self.stop_event.set()
