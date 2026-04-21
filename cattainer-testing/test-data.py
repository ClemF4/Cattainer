import logging
from picamera2 import Picamera2
import time
from datetime import datetime
from libcamera import Transform
import sys
import os

# Get the absolute path of the directory this script is inside (cattainer-testing)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Build a path that goes up one level ('..') and down into 'cattainer-core'
core_dir = os.path.join(current_dir, '..', 'cattainer-core')

# Inject that folder into Python's search path
sys.path.append(core_dir)

import initialisation
import detection
import zones
import deterrant

#Initalise the camera & close the program if there is an error
def initialiseCamera2():
    #In future add redundancy so that it checks the architecture of the camera, then uses picamera if its a pi & something else if it isnt
    logging.info("Cattainer: Checking for connected cameras")
    try:
        #If the camera isnt connected this line will cause an error & go straight to except
        picam2 = Picamera2()
        #Flip camera upside down with the transform
        config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, transform=Transform(hflip=1, vflip=1))
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


if __name__ == "__main__":
    #picam2 = initialisation.initialiseCamera()
    picam2 = initialiseCamera2()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    picam2.start_and_record_video(f"test-recordings/video_{timestamp}.mp4", duration=10)