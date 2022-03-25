import cv2
import os

from datetime import datetime

from config import SwatchConfig
from const import CONST_MEDIA_DIR

def save_snapshot(name, image):
    time = datetime.now()

    file_dir = f"{CONST_MEDIA_DIR}/snapshots/{time.strftime('%m-%d')}"
    file = f"{name}_{time.strftime('%f')}.jpg"
    cv2.imwrite(f"{file_dir}/{file}", image)