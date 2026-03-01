import time
import cv2
import os
from picamera2 import Picamera2

OUTPUT_DIR = 'output_frames'

def run_test():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    print("Initializing Picamera2...")
    # 1. Boot up the official Pi Camera library
    picam2 = Picamera2()
    
    # 2. Configure the camera for standard 640x480 resolution
    # We ask for RGB888 format which is standard for AI/Math arrays
    config = picam2.create_video_configuration(main={"size": (640, 480), "format": "RGB888"})
    picam2.configure(config)
    picam2.start()
    
    print("Warming up camera sensor...")
    time.sleep(2)
    
    for i in range(5):
        # 3. Grab the frame directly into a mathematical Numpy array!
        frame_rgb = picam2.capture_array()
        
        # 4. Convert Raspberry Pi's RGB format into OpenCV's BGR format
        frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
        
        filename = os.path.join(OUTPUT_DIR, f"test_frame_{i}.jpg")
        cv2.imwrite(filename, frame_bgr)
        print(f"Saved: {filename}")
        
        time.sleep(0.5)

    # 5. Safely shut down the hardware
    picam2.stop()
    print("Test complete. Camera released.")

if __name__ == "__main__":
    run_test()