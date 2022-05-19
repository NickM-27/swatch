"""Database models."""

from peewee import (
    Model,
    CharField,
    DateTimeField,
    FloatField,
)

class Detection(Model):  # type: ignore[misc]
    """Detections that are tracked."""
    id = CharField(null=False, primary_key=True, max_length=30)
    label = CharField(index=True, max_length=20)
    camera = CharField(index=True, max_length=20)
    zone = CharField(index=True, max_length=20)
    color_variant = CharField(index=True, max_length=20)
    start_time = DateTimeField()
    end_time = DateTimeField()
    top_area = FloatField()
