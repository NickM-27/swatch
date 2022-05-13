"""Configuration for SwatchApp."""

from __future__ import annotations

from enum import Enum
from pydantic import BaseModel, Extra, Field
import yaml


class SwatchBaseModel(BaseModel):
    """Base config that sets rules."""
    class Config:
        extra = Extra.forbid


class SnapshotModeEnum(str, Enum):
    """Types of snapshots to retain."""
    all = "all"
    crop = "crop"
    mask = "mask"


class SnapshotConfig(SwatchBaseModel):
    """Config for saving snapshots."""
    save_detections: bool = Field(
        title="Save snapshots of detections that are found.", default=True
    )
    save_misses: bool = Field(
        title="Save snapshots of missed detections.", default=False
    )
    snapshot_mode: SnapshotModeEnum = Field(
        title="Snapshot mode.", default=SnapshotModeEnum.all
    )


class ColorConfig(SwatchBaseModel):
    """Configuration of color values."""
    color_lower: str = Field(title="Lower R, G, B color values")
    color_upper: str = Field(title="Higher R, G, B color values")


class ObjectConfig(SwatchBaseModel):
    """Configuration of the object detection."""
    color_variants: dict[str, ColorConfig] = Field(
        title="Color variants for this object", default_factory=dict
    )
    min_area: int = Field(title="Min Area", default=0)
    max_area: int = Field(title="Max Area", default=240000)


class ZoneConfig(SwatchBaseModel):
    """Configuration for cropped parts of camera frame."""
    coordinates: str = Field(title="Coordinates polygon for the defined zone.")
    objects: list[str] = Field(title="Included Objects.")
    snapshot_config: SnapshotConfig = Field(
        title="Snapshot config for this zone.", default_factory=SnapshotConfig
    )


class CameraConfig(SwatchBaseModel):
    """Configuration for camera."""
    name: str | None = Field(title="Camera name.", regex="^[a-zA-Z0-9_-]+$")
    snapshot_url: str = Field(title="Camera Snapshot Url.", default=None)
    auto_detect: int = Field(
        title="Frequency to automatically run detection.", default=0
    )
    zones: dict[str, ZoneConfig] = Field(
        default_factory=dict, title="Zones for this camera."
    )


class SwatchConfig(SwatchBaseModel):
    """Main configuration for SwatchApp."""
    objects: dict[str, ObjectConfig] = Field(title="Object configuration.")
    cameras: dict[str, CameraConfig] = Field(title="Camera configuration.")

    @property
    def runtime_config(self) -> SwatchConfig:
        """Merge camera config with globals."""
        config = self.copy(deep=True)

        for name, camera in config.cameras.items():
            camera_dict = camera.dict(exclude_unset=True)
            camera_config: CameraConfig = CameraConfig.parse_obj(
                {"name": name, **camera_dict}
            )

            config.cameras[name] = camera_config

        return config

    @classmethod
    def parse_file(cls, path):  # type: ignore[no-untyped-def]
        """Parses and raw file to return config."""
        with open(path) as f:
            raw_config = f.read()

        config = yaml.safe_load(raw_config)
        return cls.parse_obj(config)
