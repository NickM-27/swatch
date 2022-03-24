import requests
import cv2
import numpy as np
import os
from os import listdir

from config import SwatchConfig

class SwatchService():

    def __init__(self):
        print("SwatchService Starting")
        self.init_config()
    
    def __check_image__(self, crop):
        lower = np.array([70, 70, 0], dtype="uint8")
        upper = np.array([110, 100, 50], dtype="uint8")

        mask = cv2.inRange(crop, lower, upper)
        output = cv2.bitwise_and(crop, crop, mask=mask)
        matches = np.count_nonzero(output)

        if matches > 1000:
            return (True, matches)
        else:
            return (False, matches)
    
    def detect(self, camera_name, image_url):
        imgBytes = requests.get(image_url).content
        img = cv2.imdecode(np.asarray(bytearray(imgBytes), dtype=np.uint8), -1)

        if img.size > 0:
            crop = img[540:620, 225:350]
        else:
            crop = []

        if crop.size <= 0:
            return None

        return self.__check_image__(crop)
    
    def init_config(self):
        print("Importing config")
        config_file = "config/config.yaml"

        if os.path.isfile(config_file):
            print("Verified")

        user_config = SwatchConfig.parse_file(config_file)
        self.config = user_config.runtime_config