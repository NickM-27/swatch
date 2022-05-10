import unittest
import numpy as np
from pydantic import ValidationError

from swatch.config import (
    SwatchConfig,
)


class TestConfig(unittest.TestCase):
    def simple_setup(self) -> None:
        self.minimal = {
            "objects": {
                "test_obj": {
                    "color_lower": "1, 1, 1",
                    "color_upper": "2, 2, 2",
                    "min_area": 0,
                    "max_area": 100000,
                },
            },
            "cameras": {
                "test_cam": {
                    "snapshot_url": "http://localhost/snap.jpg",
                    "zones": {
                        "test_zone": {
                            "coordinates": "1, 2, 3, 4",
                            "object": ["test_obj"],
                        },
                    },
                },
            },
        }

    def test_config_class(self) -> None:
        swatch_config = SwatchConfig(**self.minimal)
        assert self.minimal == swatch_config.dict(exclude_unset=True)
