import cv2
import os

from datetime import datetime

from config import SwatchConfig
from const import CONST_MEDIA_DIR


def save_snapshot(name, image):
    time = datetime.now()

    file_dir = f"{CONST_MEDIA_DIR}/snapshots/{time.strftime('%m-%d')}"

    if not os.path.exists(file_dir):
        print(f"{file_dir} doesn't exist, creating...")
        os.makedirs(file_dir)
        print(f"after creating {os.listdir('/media/')}")

    file = f"{file_dir}/{name}_{time.strftime('%f')}.jpg"
    cv2.imwrite(file, image)
