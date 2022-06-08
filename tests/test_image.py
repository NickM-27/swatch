"""Tests for SwatchImage"""

import unittest

from swatch.config import SwatchConfig


class TestImage(unittest.TestCase):
    """Testing the configuration is parsed correctly."""

    def setUp(self) -> None:
        """setup simple"""
        self.config = {
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

    def test_valid_time_range(self) -> None:
        swatch_config = SwatchConfig(**self.config)
        now_time = "12:00"
        color_variant = swatch_config.objects["test_obj"].color_variants["default"]
        assert (
            now_time < color_variant.time_range.after
            or now_time > color_variant.time_range.before
        )

    def test_invalid_time_range(self) -> None:
        swatch_config = SwatchConfig(**self.config)
        now_time = "04:00"
        color_variant = swatch_config.objects["test_obj"].color_variants["default"]
        assert not (
            now_time < color_variant.time_range.after
            or now_time > color_variant.time_range.before
        )
