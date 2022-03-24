from pydantic import BaseModel, Extra, Field, validator
from os import listdir
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

    @classmethod
    def parse_file(cls, config_file):
        print(f"Doing thing {listdir('./')} and config {listdir('config')}")
        with open(config_file) as f:
            raw_config = f.read()
            
        config = yaml.safe_load(raw_config)
        return cls.parse_obj(config)