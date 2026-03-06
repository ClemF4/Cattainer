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
    logging.info("Cattainer: Checking for connected cameras")
    try:
        #If the camera isnt connected this line will cause an error & go straight to except
        picam2 = Picamera2()
        config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
        picam2.configure(config)
        picam2.start()
        #Sleep the camera for 2 seconds while it calculates the lighting
        time.sleep(2)
        logging.info("Cattainer: Camera found & initalised successfully")
        return picam2

    except Exception as e:
        #Add these errors to the log if the camera is disconnected
        logging.error("Cattainer: Camera not found or unable to initalise")
        logging.error(f"Cattainer: Camera error details: {e}")
        sys.exit(1)

def initaliseTPU():
    logging.info("Cattainer: Checking if the TPU is connected")
    try:
        #If the Coral is disconnected then it'll throw an error
        model = YOLO("model_edgetpu.tflite")
        logging.info("Cattainer: YOLO model has been correctly initalised on the TPU")
        return model
    except Exception as e:
        logging.error("Cattainer: Unable to load model, check whether the Coral has had a brownout, unplug & replug")
        logging.error(f"Cattainer: Model error details: {e}")
        sys.exit(1)

def catDetect(picam2, model):
    return

if __name__ == "__main__":
    #Initialise Camera & TPU
    picam2 = initialiseCamera()
    model = initaliseTPU()

    #Infinite Loop
    while(True):
        catDetect(picam2, model)
        