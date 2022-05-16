"""Swatch service."""

import threading

from swatch.app import SwatchApp

threading.current_thread().name = "swatch"

if __name__ == "__main__":
    swatch_app = SwatchApp()
    swatch_app.start()
