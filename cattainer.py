import cv2
import time
import os
from ultralytics import YOLO

# --- CONFIGURATION ---
MODEL_PATH = 'model_edgetpu.tflite' # Must match your file name
TEST_MEDIA = 'tests/test_video.mp4'  # Put a video here (or use 'tests/test.jpg')
OUTPUT_PATH = 'output/test_result.avi' # Where to save the result
# ---------------------

def run_test():
    print(f"--- STARTING CONTAINER TEST ---")
    
    # 1. Check if Model Exists
    if not os.path.exists(MODEL_PATH):
        print(f"ERROR: Model not found at {MODEL_PATH}")
        return

    # 2. Load the Coral Model
    try:
        print(f"Loading Model: {MODEL_PATH}...")
        start_time = time.time()
        # task='detect' is crucial for TFLite models
        model = YOLO(MODEL_PATH, task='detect') 
        print(f"Model Loaded successfully in {time.time() - start_time:.2f}s")
    except Exception as e:
        print(f"ERROR Loading Model: {e}")
        print("   (Check if Coral USB stick is plugged in and passed to Docker)")
        return

    # 3. Open Video Source
    cap = cv2.VideoCapture(TEST_MEDIA)
    if not cap.isOpened():
        print(f"ERROR: Could not open media: {TEST_MEDIA}")
        return

    # Get video properties for saving
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps    = cap.get(cv2.CAP_PROP_FPS) or 30

    # Create Video Writer
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    out = cv2.VideoWriter(OUTPUT_PATH, cv2.VideoWriter_fourcc(*'MJPG'), fps, (width, height))
    
    print(f"Processing video: {TEST_MEDIA} ({width}x{height} @ {fps}fps)")
    print(f"Saving result to: {OUTPUT_PATH}")

    frame_count = 0
    start_proc = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break # End of video

        # 4. RUN INFERENCE (The critical part)
        # imgsz=320 is required for your specific compiled model
        results = model(frame, imgsz=320, verbose=False)

        # 5. Draw Boxes
        annotated_frame = results[0].plot()

        # Write to output video
        out.write(annotated_frame)
        
        frame_count += 1
        if frame_count % 10 == 0:
            print(f"Processed {frame_count} frames...", end='\r')

    cap.release()
    out.release()
    
    total_time = time.time() - start_proc
    print(f"\nTEST COMPLETE!")
    print(f"Processed {frame_count} frames in {total_time:.2f}s ({frame_count/total_time:.1f} FPS)")
    print(f"Check your output file: {OUTPUT_PATH}")

if __name__ == "__main__":
    run_test()