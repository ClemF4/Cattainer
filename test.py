from ultralytics import YOLO

# --- CONFIGURATION ---
# Use the filename of the model you exported for Edge TPU
MODEL_PATH = 'best_full_integer_quant_edgetpu.tflite' 
IMAGE_PATH = 'tests/test (1).png'
# ---------------------

print("Loading model... (This might take a moment on the Pi)")
# The task='detect' is important so it knows how to handle the output
model = YOLO(MODEL_PATH, task='detect')

print(f"Running inference on {IMAGE_PATH}...")
# Run prediction
# imgsz=320 is CRITICAL because you compiled it for this size
# conf=0.5 means "only tell me if you are 50% sure"
results = model.predict(IMAGE_PATH, imgsz=320, conf=0.5)

# --- PRINT RESULTS TO TERMINAL ---
print("\n--- RESULTS ---")
for result in results:
    boxes = result.boxes  # Get the boxes
    for box in boxes:
        # Get the class ID (0 or 1)
        class_id = int(box.cls[0])
        # Get the confidence score
        conf = float(box.conf[0])
        # Get the class name (if embedded) or use the ID
        name = result.names[class_id]
        
        print(f"Found: {name} | Confidence: {conf:.2f}")

    # Save the resulting image with boxes drawn
    result.save(filename='result.jpg')
    print(f"\nSaved annotated image to: result.jpg")