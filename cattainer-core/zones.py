import logging
import json
import sys
import deterrant
import numpy as np
import cv2
import deterrant


logger = logging.getLogger(__name__)


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
                    deterrant.triggerUltrasonic()
                    break #Stops function immediatly
                elif zoneType == "amber" and label == "cat_jumping":
                    #If the cat is in the amber zone & is jumping trigger deterrant
                    deterrant.triggerUltrasonic()
                    break  
