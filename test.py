import cv2
import time
import os
from ultralytics import YOLO

# Configuration
MODEL_PATH = 'model_edgetpu.tflite'
TEST_MEDIA = 'tests/test_video.mp4'
OUTPUT_DIR = 'output_frames' 

def run_test():
    print(f"--- STARTING IMAGE TEST ---")
    
    # Load Model
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Error: Model not found at {MODEL_PATH}")
        return

    try:
        print(f"Loading Model: {MODEL_PATH}...")
        model = YOLO(MODEL_PATH, task='detect') 
        print(f"✅ Model Loaded!")
    except Exception as e:
        print(f"❌ Error Loading Model: {e}")
        return

    # Open Video
    cap = cv2.VideoCapture(TEST_MEDIA)
    if not cap.isOpened():
        print(f"❌ Error: Could not open video: {TEST_MEDIA}")
        return

    # Create output folder
    if os.path.exists(OUTPUT_DIR):
        import shutil
        shutil.rmtree(OUTPUT_DIR) # Clean old run
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print(f"Saving detected frames to: {OUTPUT_DIR}/")

    frame_count = 0
    saved_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run Inferance
        # We process every frame to test speed, but only save some
        results = model(frame, imgsz=320, verbose=False)

        frame_count += 1
        
        # Save Image Logic
        # Save the first frame, and then every 30th frame (approx every 1 second)
        if frame_count == 1 or frame_count % 30 == 0:
            # Draw boxes
            annotated_frame = results[0].plot()
            
            filename = f"{OUTPUT_DIR}/frame_{frame_count:04d}.jpg"
            cv2.imwrite(filename, annotated_frame)
            saved_count += 1
            print(f"Saved {filename} | Cats found: {len(results[0].boxes)}")

    cap.release()
    print(f"\nDone Saved {saved_count} images to '{OUTPUT_DIR}' folder.")

if __name__ == "__main__":
    run_test()