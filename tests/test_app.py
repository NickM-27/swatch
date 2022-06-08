"""Tests for SwatchApp"""

import os
import unittest

from swatch.app import SwatchApp


class TestApp(unittest.TestCase):
    """Testing the configuration is parsed correctly."""

    def setUp(self) -> None:
        """setup simple"""
        self.db_file = "/media/databases/swatch.db"

    def test_db_created(self) -> None:
        app = SwatchApp()
        assert not os.path.exists(self.db_file)
        os.environ["DB_FILE"] = self.db_file
        app.__init_db__()
        assert os.path.exists(self.db_file)


