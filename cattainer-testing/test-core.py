import sys
import os
import time
import logging
from logging.handlers import RotatingFileHandler

#Create a loghandler which makes sure the log doesnt become huge after days of this script running 
logHandler = RotatingFileHandler(
    filename='cattainer.log',
    maxBytes=5 * 1024 * 1024, #5 megabytes (5 * 1024 kb * 1024 bytes)
    backupCount=2
)

#Setup the loggers name, format, and level (change the level to warning when in production to ignore all the info logs)
logging.basicConfig(
    level = logging.INFO, #This allows warning logs & anything more severe into the log
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logHandler]
)

# Get the absolute path of the directory this script is inside (cattainer-testing)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build a path that goes up one level ('..') and down into 'cattainer-core'
core_dir = os.path.join(current_dir, '..', 'cattainer-core')

# Inject that folder into Python's search path
sys.path.append(core_dir)


import zones # type: ignore
import initialisation # type: ignore
import deterrent # type: ignore
import cv2
import json
import numpy as np


#Perform the logic of capturing a frame, running the model, and returning the correct output based on the model output
def catDetect(frame, model):
    #Run inference on the frame
    output = model(frame, imgsz=320, verbose=False)
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
    logging.info("Cattainer: Loading savedZones.json")
    try:
        with open("/home/cattainer/Cattainer/cattainer-data/savedZones.json", "r") as file:
            zonesData = json.load(file)

            #Check if zoneData is empty
            if zonesData == 0:
                logging.error("Cattainer: No Zones found, please draw zones in the web UI")
                sys.exit(1)
            
            #Format the JSON zones by removing the x: and y: strings, and move the points into a formatted array
            formattedZones = []
            for zone in zonesData:
                rawPoints = zone["coordinates"]
                zoneType = zone["zoneType"]
                polygonArray = np.array([[point["x"], point["y"]] for point in rawPoints], dtype=np.int32)
                #Use a dictionary to append the zoneType and formatted polygons
                formattedZones.append({"zoneType": zoneType, "polygonArray": polygonArray})
            logging.info(f"Cattainer: Loaded {len(zonesData)} zones successfully")
            return formattedZones
        
    except FileNotFoundError:
        logging.error("Cattainer: savedZones.json file not found, please redraw the zones")
        sys.exit(1)



if __name__ == "__main__":
    model = initialisation.initaliseTPU()
    #Read the saved_zones.json
    formattedZones = loadZones()
    #Check the time that the json file was last edited
    deterrentActive = False
    deterrentLastTriggered = time.time()
    video = "video_20260423_140337"
    inputVideo = f"test-recordings/{video}.mp4"

    # read the video
    cap = cv2.VideoCapture(inputVideo)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break # Video is over

        # Convert colors to RGB for YOLO
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        targets = catDetect(rgb_frame, model)

        if len(targets) == 0:
            if ((time.time() - deterrentLastTriggered > 2) and (deterrentActive == True)):
                deterrent.resetUltrasonic()
                deterrentActive = False
            continue #This restarts the while loop
        deterrentActive = zones.zoneLogic(targets, formattedZones)
        if deterrentActive == True:
            deterrentLastTriggered = time.time()
    cap.release()