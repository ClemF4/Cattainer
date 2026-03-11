import logging
from logging.handlers import RotatingFileHandler
import sys
import os
import detection
import zones
import initialisation
import deterrant

#Create a loghandler which makes sure the log doesnt become huge after days of this script running 
logHandler = RotatingFileHandler(
    filename='cattainer.log',
    maxBytes=5 * 1024 * 1024, #5 megabytes (5 * 1024 kb * 1024 bytes)
    backupCount=2
)

#Setup the loggers name, format, and level (change the level to warning when in production to ignore all the info logs)
logging.basicConfig(
    level = logging.WARNING, #This allows warning logs & anything more severe into the log
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logHandler]
)


if __name__ == "__main__":
    #Initialise Camera & TPU
    picam2 = initialisation.initialiseCamera()
    model = initialisation.initaliseTPU()
    #Read the saved_zones.json
    zonesData = zones.loadZones()
    #Check the time that the json file was last edited
    lastKnownTime = os.path.getmtime("data/saved_zones.json")

    #Infinite Loop
    while(True):
        #Check the last time that the zones were loaded
        currentKnownTime = os.path.getmtime("data/saved_zones.json")
        #Reload the zones if needed
        if currentKnownTime != lastKnownTime:
            zonesData = zones.loadZones()
            logging.info("Cattainer: New zones detected, reloading zones")
            lastKnownTime = currentKnownTime
        #Run inference
        targets = detection.catDetect(picam2, model)
        #Check if a box with confidence>60% has been found
        if len(targets) == 0:
            continue #This restarts the while loop
        zones.zoneLogic(targets, zonesData)
