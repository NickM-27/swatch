from __future__ import annotations

from typing import Dict, List, Optional, Tuple, Union
from pydantic import BaseModel, Extra, Field, validator
import yaml

class SwatchBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid


class ObjectConfig(SwatchBaseModel):
    color_lower: Union[str, List[str]] = Field(
        title="Lower R, G, B color values"
    )
    color_upper: str = Field(title="Higher R, G, B color values")
    min_area: int = Field(title="Min Area", default=0)
    max_area: int = Field(title="Max Area", default=240000)


class ZoneConfig(SwatchBaseModel):
    coordinates: Union[str, List[str]] = Field(
        title="Coordinates polygon for the defined zone."
    )
    objects: List[str] = Field(title="Included Objects.")


class CameraConfig(SwatchBaseModel):
    zones: Dict[str, ZoneConfig] = Field(
        default_factory=dict, title="Zones for this camera."
    )


class SwatchConfig(SwatchBaseModel):
    objects: Dict[str, ObjectConfig] = Field(title="Object configuration.")
    cameras: Dict[str, CameraConfig] = Field(title="Camera configuration.")

    @property
    def runtime_config(self) -> SwatchConfig:
        """Merge camera config with globals."""
        config = self.copy(deep=True)
        return config

    @classmethod
    def parse_file(cls, config_file):
        with open(config_file) as f:
            raw_config = f.read()
            
        config = yaml.safe_load(raw_config)
        return cls.parse_obj(config)