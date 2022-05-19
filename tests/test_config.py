"""Tests for SwatchConfig"""

import unittest

from swatch.config import SwatchConfig


class TestConfig(unittest.TestCase):
    """Testing the configuration is parsed correctly."""

    def setUp(self) -> None:
        """setup simple"""
        self.minimal = {
            "objects": {
                "test_obj": {
                    "color_variants": {
                        "default": {
                            "color_lower": "1, 1, 1",
                            "color_upper": "2, 2, 2",
                        },
                    },
                    "min_area": 0,
                    "max_area": 100000,
                },
            },
            "cameras": {
                "test_cam": {
                    "snapshot_config": {
                        "url": "http://localhost/snap.jpg",
                    },
                    "zones": {
                        "test_zone": {
                            "coordinates": "1, 2, 3, 4",
                            "objects": ["test_obj"],
                        },
                    },
                },
            },
        }
        self.full = {
            "objects": {
                "test_obj": {
                    "color_variants": {
                        "default": {
                            "color_lower": "1, 1, 1",
                            "color_upper": "2, 2, 2",
                            "time_range": {
                                "after": "08:00",
                                "before": "18:00",
                            },
                        },
                    },
                    "min_area": 0,
                    "max_area": 100000,
                },
            },
            "cameras": {
                "test_cam": {
                    "auto_detect": 300,
                    "snapshot_config": {
                        "url": "http://localhost/snap.jpg",
                        "save_detections": True,
                        "save_misses": True,
                        "mode": "mask",
                        "retain_days": 100,
                    },
                    "zones": {
                        "test_zone": {
                            "coordinates": "1, 2, 3, 4",
                            "objects": ["test_obj"],
                        },
                    },
                },
            },
        }

    def test_minimal_config_class(self) -> None:
        swatch_config = SwatchConfig(**self.minimal)
        assert self.minimal == swatch_config.dict(exclude_unset=True)

    def test_full_config_class(self) -> None:
        swatch_config = SwatchConfig(**self.full)
        assert self.full == swatch_config.dict(exclude_unset=True)
