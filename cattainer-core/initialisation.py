import logging
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO
import sys
import time

logger = logging.getLogger(__name__)

#Initalise the camera & close the program if there is an error
def initialiseCamera():
    #In future add redundancy so that it checks the architecture of the camera, then uses picamera if its a pi & something else if it isnt
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


#Initalise the TPU & close the program if either the .tflite file doesnt exist or if the model was loaded on the CPU instead of TPU
def initaliseTPU():
    logging.info("Cattainer: Checking if the TPU is connected")
    try:
        #If the model isnt there this will throw an error
        model = YOLO("model_edgetpu.tflite", task="detect")
        logging.info("Cattainer: YOLO model has been loaded (Device unsure)")
        #Run dummy inference to ensure that the model is on the Coral & not the CPU
        dummyFrame = np.zeros((480,640,3), dtype=np.uint8)
        #Run model once to build the YOLO pipeline (since the first run always takes a long time)
        model(dummyFrame)
        #Now time how long inference takes once the pipeline has already been build, this gives an accurate time
        startTime = time.time()
        model(dummyFrame)
        endTime = time.time()
        totalTime = endTime - startTime
        # Check whether the time taken was long, since this indicated whether it was CPU or TPU
        if totalTime>0.5:
            logging.error("Cattainer: Model was loaded onto the CPU not the Coral")
            sys.exit(1)
        logging.info("Cattainer: YOLO model has been correctly initalised on the TPU")
        return model
    
    except Exception as e:
        logging.error("Cattainer: Unable to load model, check whether the Coral has had a brownout, unplug & replug")
        logging.error(f"Cattainer: Model error details: {e}")
        sys.exit(1)