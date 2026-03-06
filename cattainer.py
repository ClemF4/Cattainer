import time
import cv2
import os
import sys
import logging
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO


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

def catDetect(picam2, model):
    #Capture a single frame
    frame = picam2.capture_array()
    #Check if the flag file is present
    if os.path.exists("trigger_snapshot.flag"):
        logging.info("Cattainer: snapshot flag is present, saving current frame to /static/background.png")
        #Save the frame to /static/background.png
        correctedFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite("static/background.png", correctedFrame)
        os.remove("trigger_snapshot.flag")

    #Run inference on the frame
    output = model(frame, imgsz=320, )
    #Extract the first output as our result since YOLO returns a list 
    result = output[0]
    #Find the bounding boxes
    boxes = result.boxes
    #Check if the model actually found anything 
    if len(boxes)>0:
        confidence = boxes.conf[0].item()
        coords = boxes.xywh[0].tolist()

        if confidence > 0.6:
            logging.info("Cattainer: Found an object with confidence > 60%")
            logging.info(f"Cattainer: Bounding box center coordinates: {coords}")
            return coords
        logging.info("Cattainer: Found an object however confidence is < 60%")
    logging.info("Cattainer: No object found")
    return 0

if __name__ == "__main__":
    #Initialise Camera & TPU
    picam2 = initialiseCamera()
    model = initaliseTPU()
    
    #Infinite Loop
    while(True):
        coords = catDetect(picam2, model) #TESTING THE FUNCTION ONCE, NOT IN A LOOP
        #Check if a box with confidence>60% has been found
        if coords == 0:
            #This restarts the while loop
            continue
        
        