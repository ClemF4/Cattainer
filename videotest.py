from ultralytics import YOLO

# --- CONFIGURATION ---
MODEL_PATH = 'best_full_integer_quant_edgetpu.tflite'
INPUT_VIDEO = 'tests/jumptest.mp4' # Your input video file
# ---------------------

print("Loading model... (This might take a moment on the Pi)")
model = YOLO(MODEL_PATH, task='detect')

print(f"Processing video: {INPUT_VIDEO}...")

# --- RUN INFERENCE ---
# source=INPUT_VIDEO: Tells YOLO to read the video file
# save=True: Tells YOLO to save a new video file with the boxes drawn
# stream=True: CRITICAL for Pi. It processes one frame at a time (generator) 
#              rather than loading the whole video into RAM.
results = model.predict(
    source=INPUT_VIDEO, 
    imgsz=320, 
    conf=0.5, 
    save=True, 
    stream=True
)

print("\n--- PROCESSING FRAMES ---")
# We iterate through the results generator. 
# The processing actually happens *during* this loop.
for i, result in enumerate(results):
    # Optional: Print info every 30 frames to show it's working without spamming
    if i % 30 == 0:
        print(f"Processed frame {i}...")

print(f"\nProcessing complete.")
print(f"Results saved to the 'runs/detect/predict' folder.")