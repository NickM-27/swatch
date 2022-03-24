from __future__ import annotations

from pydantic import BaseModel, Extra, Field, validator
import yaml

class SwatchBaseModel(BaseModel):
    class Config:
        extra = Extra.forbid

class CameraConfig(SwatchBaseModel):
    test: str = Field(title="")

class SwatchConfig(SwatchBaseModel):
    camera: CameraConfig = Field(
        default_factory=CameraConfig,
        title="Camera"
    )

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