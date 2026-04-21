import logging
import requests
import time

logger = logging.getLogger(__name__)

#Hardcoded IP for testing
HA_WEBHOOK_URL = "http://192.168.1.72:8123/api/webhook/cattainer_incoming_data"


#Trigger the deterrant (Ultrasonic Device) & Send Notification
def triggerUltrasonic():
    logging.info("Cattainer: TRIGGERING DETERRANT")

    try:
        # payload is what binary_sensor.py expects
        payload = {"cat_detected": True}

        #send post request & have 5 second timeout
        response = requests.post(HA_WEBHOOK_URL, json=payload, timeout=5)

        if response.status_code == 200:
            logging.info("Cattainer: Sucessfully sent webhook to Home Assistant Server")
            payload = {"cat_detected": False}
            response = requests.post(HA_WEBHOOK_URL, json=payload, timeout=5)


        else:
            logging.error(f"Cattainer: Webhook failed with status code: {response.status_code}")

    except:
        logging.error(f"Cattainer: Failed to connect to Home Assistant Webhook: {requests.exceptions.RequestException}")   

    return