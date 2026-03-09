import time
import cv2
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import json
import numpy as np
from picamera2 import Picamera2
from ultralytics import YOLO

#Create a loghandler which makes sure the log doesnt become huge after days of this script running 
logHandler = RotatingFileHandler(
    filename='cattainer.log',
    maxBytes=5 * 1024 * 1024, #5 megabytes (5 * 1024 kb * 1024 bytes)
    backupCount=2
)

#Setup the loggers name, format, and level (change the level to warning when in production to ignore all the info logs)
logging.basicConfig(
    level = logging.INFO, #This allows info logs & anything more severe into the log (change to warning when complete to only log important stuff)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logHandler,
    logging.StreamHandler(sys.stdout)]
)


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


#Perform the logic of capturing a frame, running the model, and returning the correct output based on the model output
def catDetect(picam2, model):
    #Capture a single frame
    frame = picam2.capture_array()
    #Check if the flag file is present
    if os.path.exists("data/trigger_snapshot.flag"):
        logging.info("Cattainer: snapshot flag is present, saving current frame to data/static/background.png")
        #Save the frame to data/static/background.png
        correctedFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imwrite("data/static/background.png", correctedFrame)
        os.remove("data/trigger_snapshot.flag")

    #Run inference on the frame
    output = model(frame, imgsz=320, )
    #Extract the first output as our result since YOLO returns a list 
    result = output[0]
    #Find the bounding boxes
    boxes = result.boxes
    #Create an empty array which will be returned to main
    highConfBoxes = []
    #Check if the model actually found anything 
    if len(boxes)>0:
        #Iterate through every box & check if they are high confidence
        for box in boxes:
            confidence = box.conf.item()
            if confidence > 0.6:
                logging.info("Cattainer: Found an object with confidence > 60%")
                #Extract the coords
                coords = box.xywh[0].tolist()
                #Extract the class
                classID = int(box.cls.item())
                label = result.names[classID]
                logging.info(f"Cattainer: Bounding box center coordinates: {coords}, Lables: {label}")
                highConfBoxes.append((coords, label))
    if len(highConfBoxes) == 0:    
        logging.info("Cattainer: Did not find any objects with confidence > 60%")
    return highConfBoxes


#Load the zones from the .json into a variable
def loadZones():
    logging.info("Cattainer: Loading saved_zones.json")
    try:
        with open("data/saved_zones.json", "r") as file:
            zonesData = json.load(file)
            if zonesData == 0:
                logging.error("Cattainer: No Zones found, please draw zones in the web UI")
                sys.exit(1)
            logging.info(f"Cattainer: Loaded {len(zonesData)} zones successfully")
            return zonesData
    except FileNotFoundError:
        logging.error("Cattainer: saved_zones.json file not found, please redraw the zones")
        sys.exit(1)


#Compare the current cat position to the zones
def zoneLogic(targets, zonesData):
    #Pull the array & label of each box from out of the tuple one at a time
    for coords, label in targets:
        #Find the center x,y coords of the cat
        catCenter = (coords[0], coords[1])
        for zone in zonesData:
            #Find the zone type & extract the raw coordinates of this zone
            zoneType = zone["zoneType"]
            rawPoints = zone["coordinates"]
            #Format the points (remove the "x" & "y" and just keep the numbers)
            formattedPoints =[]
            for point in rawPoints:
                xVal = point["x"]
                yVal = point["y"]
                formattedPoints.append([xVal, yVal])
            #Format these points into a format which cv2.pointPolygonTest accepts as an input
            polygonArray = np.array(formattedPoints, dtype=np.int32)
            #Use opencv's function, this checks whether the catCenter points are within polygonArray, the 3rd argument is set to false since we dont care about the distance from the point to the polygon
            isInside = cv2.pointPolygonTest(polygonArray, catCenter, False)
            #Returns 1 if inside, 0 if on border, and -1 if outside
            if isInside >= 0:
                logging.info(f"Cattainer: The {label} is inside the: {zoneType}")
                if zoneType == "red":
                    #If the cat is in the red zone trigger deterrant
                    triggerDeterrant()
                    break #Stops function immediatly
                elif zoneType == "amber" and label == "cat_jumping":
                    #If the cat is in the amber zone & is jumping trigger deterrant
                    triggerDeterrant()
                    break
                

#Trigger the deterrant (Ultrasonic Device)
def triggerDeterrant():
    logging.info("Cattainer: TRIGGERING DETERRANT")
    return


if __name__ == "__main__":
    #Initialise Camera & TPU
    picam2 = initialiseCamera()
    model = initaliseTPU()
    #Read the saved_zones.json
    zonesData = loadZones()
    #Check the time that the json file was last edited
    lastKnownTime = os.path.getmtime("data/saved_zones.json")

    #Infinite Loop
    while(True):
        #Check the last time that the zones were loaded
        currentKnownTime = os.path.getmtime("data/saved_zones.json")
        #Reload the zones if needed
        if currentKnownTime != lastKnownTime:
            zonesData = loadZones()
            logging.info("Cattainer: New zones detected, reloading zones")
            lastKnownTime = currentKnownTime
        #Run inference
        targets = catDetect(picam2, model)
        #Check if a box with confidence>60% has been found
        if len(targets) == 0:
            continue #This restarts the while loop
        zoneLogic(targets, zonesData)
