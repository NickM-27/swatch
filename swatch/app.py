"""Main SwatchApp responsible for running the app."""
import logging
import os
import multiprocessing
import signal
import sys
from typing import Dict, Optional
from types import FrameType

from peewee_migrate import Router
from playhouse.sqlite_ext import SqliteExtDatabase
from playhouse.sqliteq import SqliteQueueDatabase

from swatch.config import SwatchConfig
from swatch.const import CONST_CONFIG_FILE, CONST_DB_FILE
from swatch.http import create_app
from swatch.image import ImageProcessor
from swatch.detection import AutoDetector, DetectionCleanup
from swatch.models import Detection
from swatch.snapshot import SnapshotCleanup, SnapshotProcessor


class SwatchApp:
    """Main swatch process that handles the lifecycle of the app."""

    def __init__(self) -> None:
        """Init SwatchApp."""
        logging.info("Starting SwatchApp")
        self.stop_event = multiprocessing.Event()
        # startup nginx
        os.system("/usr/local/nginx/sbin/nginx &")

        # startup internal processes
        try:
            self.__init_config__()
        except Exception as e:
            logging.error("Error parsing config file\n%s", e)
            self.stop()
            return

        self.__init_db__()
        self.__init_processing__()
        self.__init_snapshot_cleanup__()
        self.__init_detection_cleanup__()
        self.__init_web_server__()

    def __init_config__(self) -> None:
        """Init SwatchApp with saved config file."""
        logging.info("Importing SwatchApp Config")

        config_file = os.environ.get("CONFIG_FILE", CONST_CONFIG_FILE)

        if os.path.isfile(config_file):
            logging.info("Verified SwatchApp Config")

        user_config = SwatchConfig.parse_file(config_file)
        self.config = user_config.runtime_config

    def __init_db__(self):
        """Init the Swatch database."""
        db_file = os.environ.get("DB_FILE", CONST_DB_FILE)

        if not os.path.exists(db_file):
            logging.debug("%s doesn't exist, creating...", db_file)
            os.makedirs(db_file)

        swatch_db = SqliteExtDatabase(db_file)

        router = Router(swatch_db)
        router.run()

        swatch_db.close()

        self.db = SqliteQueueDatabase(db_file)
        models = [Detection]
        self.db.bind(models)

    def __init_processing__(self) -> None:
        """Init the SwatchApp processing thread."""
        self.snapshot_processor = SnapshotProcessor(self.config)
        self.image_processor = ImageProcessor(self.config, self.snapshot_processor)

        self.camera_processes: Dict[str, AutoDetector] = {}

        for name, config in self.config.cameras.items():
            if config.auto_detect > 0 and config.snapshot_config.url:
                self.camera_processes[name] = AutoDetector(
                    self.image_processor,
                    self.snapshot_processor,
                    config,
                    self.stop_event,
                )
                self.camera_processes[name].start()

    def __init_snapshot_cleanup__(self) -> None:
        """Init the SwatchApp snapshots cleanup thread."""
        self.snapshot_cleanup = SnapshotCleanup(self.config, self.stop_event)
        self.snapshot_cleanup.start()

    def __init_detection_cleanup__(self) -> None:
        """Init the SwatchAp detections cleanup thread."""
        self.detection_cleanup = DetectionCleanup(self.config, self.stop_event)
        self.detection_cleanup.start()

    def __init_web_server__(self) -> None:
        """Init the SwatchApp web server."""
        self.http = create_app(
            self.config, self.image_processor, self.snapshot_processor
        )

    def start(self) -> None:
        """Start SwatchApp."""

        def receiveSignal(signalNumber: int, frame: Optional[FrameType]) -> None:
            self.stop()
            sys.exit()

        signal.signal(signal.SIGTERM, receiveSignal)

        try:
            self.http.run(host="127.0.0.1", port=4501, debug=False)
        except KeyboardInterrupt:
            pass

        self.stop()

    def stop(self) -> None:
        """Stop SwatchApp."""
        logging.info("Stopping SwatchApp")
        self.stop_event.set()

        if self.detection_cleanup:
            # join other processes
            self.detection_cleanup.join()
            self.snapshot_cleanup.join()

            for cam in self.config.cameras.keys():
                self.camera_processes[cam].join()

            # stop the db
            self.db.stop()
