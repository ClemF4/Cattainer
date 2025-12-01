from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n_full_integer_quant_edgetpu.tflite")  # Load an official model or custom model

# Run Prediction
model.predict("all.jpg")