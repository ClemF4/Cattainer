import logging
import cv2
import os

logger = logging.getLogger(__name__)



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