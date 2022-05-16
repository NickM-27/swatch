"""Swatch service."""

import sys
import threading

from swatch.app import SwatchApp

threading.current_thread().name = "swatch"

cli = sys.modules["flask.cli"]
cli.show_server_banner = lambda *x: None

if __name__ == "__main__":
    swatch_app = SwatchApp()
    swatch_app.start()
