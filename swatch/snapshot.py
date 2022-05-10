import cv2
import os

from datetime import datetime

from swatch.config import SwatchConfig
from swatch.const import CONST_MEDIA_DIR


def save_snapshot(name: str, image) -> bool:
    time = datetime.now()

    file_dir = f"{CONST_MEDIA_DIR}/snapshots/{time.strftime('%m-%d')}"

    if not os.path.exists(file_dir):
        print(f"{file_dir} doesn't exist, creating...")
        os.makedirs(file_dir)
        print(f"after creating {os.listdir('/media/')}")
        return False

    file = f"{file_dir}/{name}_{time.strftime('%f')}.jpg"
    cv2.imwrite(file, image)
    return True
