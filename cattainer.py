import cv2
import time
import os

# Configuration
OUTPUT_DIR = 'output_frames' 

def run_test():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created directory: {OUTPUT_DIR}")

    print("Opening camera...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open the camera. Check your USB connection!")
        return

    print("Warming up camera sensor...")
    time.sleep(2)

    frames_to_capture = 5
    print(f"Capturing {frames_to_capture} frames...")

    for i in range(frames_to_capture):
        ret, frame = cap.read()
        
        if not ret:
            print(f"Error: Failed to grab frame {i}.")
            break
            
        # Construct the file path and save the image
        filename = os.path.join(OUTPUT_DIR, f"test_frame_{i}.jpg")
        cv2.imwrite(filename, frame)
        print(f"Saved: {filename}")
        
        # Wait half a second before taking the next picture
        time.sleep(0.5)

    cap.release()
    print("Test complete. Camera released.")

if __name__ == "__main__":
    run_test()