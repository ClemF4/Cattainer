import time
import cv2
import os
import sys
import logging
from picamera2 import Picamera2
from ultralytics import YOLO

OUTPUT_DIR = 'output_frames'

logging.basicConfig(
    filename = 'cattainer.log',
    level = logging.INFO, #This allows info logs & anything more severe into the log (change to warning when complete to only log important stuff)
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def initialiseCamera():
    logging.info("Checking for connected cameras")
    try:
        #If the camera isnt connected this line will cause an error & go straight to except
        picam2 = Picamera2()
        logging.info("Camera found & initalised successfully")
        return picam2

    except Exception as e:
        #Add these errors to the log if the camera is disconnected
        logging.error("Camera not found or unable to initalise")
        logging.error(f"Camera error details: {e}")
        sys.exit(1)

def catDetect():
    return

if __name__ == "__main__":
    
    initialiseCamera()
    

    