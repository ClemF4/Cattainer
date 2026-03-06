import time
import cv2
import os
import logging
from picamera2 import Picamera2
from ultralytics import YOLO

OUTPUT_DIR = 'output_frames'

logging.basicConfig(
    filename = 'cattainer.log',
    level = logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialiseCamera():
    try:
        #If the camera isnt connected this line will cause an error & go straight to except
        picam2 = Picamera2()
        return picam2
    except:
        return

def catDetect():


if __name__ == "__main__":
    initialiseCamera()
    

    