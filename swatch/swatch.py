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
    
    def __check_image__(self, crop, object):
        lower = np.array([object.color_lower[0], object.color_lower[1], object.color_lower[2]], dtype="uint8")
        upper = np.array([object.color_upper[0], object.color_upper[1], object.color_upper[2]], dtype="uint8")

        mask = cv2.inRange(crop, lower, upper)
        output = cv2.bitwise_and(crop, crop, mask=mask)
        matches = np.count_nonzero(output)

        if matches > object.min_area and matches < object.max_area:
            return {"result": True, "area": matches}
        else:
            return {"result": False, "area": matches}
    
    def detect(self, camera_name, image_url):
        response = {}
        
        for zone in self.config.cameras[camera_name].zones:
            response[zone.name] = {}
            imgBytes = requests.get(image_url).content
            img = cv2.imdecode(np.asarray(bytearray(imgBytes), dtype=np.uint8), -1)
            
            if img.size > 0:
                crop = img[zone.coordinates[1]:zone.coordinates[3], zone.coordinates[0]:zone.coordinates[2]]
            else:
                crop = []

            if crop.size <= 0:
                continue

            for object in zone.objects:
                response[zone.name][object.name] = self.__check_image__(crop, object)
        
        return response
    
    def init_config(self):
        print("Importing config")
        config_file = "config/config.yaml"

        if os.path.isfile(config_file):
            print("Verified")

        user_config = SwatchConfig.parse_file(config_file)
        self.config = user_config.runtime_config