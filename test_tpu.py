import time
import numpy as np
import tflite_runtime.interpreter as tflite

# Load the Edge TPU delegate
try:
    delegate = tflite.load_delegate('/usr/lib/aarch64-linux-gnu/libedgetpu.so.1')
    print("✅ SUCCESS: Edge TPU Driver found!")
except Exception as e:
    print("❌ ERROR: Could not load Edge TPU driver.")
    exit(1)

# Load the model
MODEL_PATH = "yolov8n_full_integer_quant_edgetpu.tflite" 
print(f"Loading {MODEL_PATH}...")

try:
    interpreter = tflite.Interpreter(
        model_path=MODEL_PATH,
        experimental_delegates=[delegate]
    )
    interpreter.allocate_tensors()
except Exception as e:
    print("❌ ERROR: Model failed to load.")
    exit(1)

# Get input details to ensure we use the right Data Type (INT8 vs FLOAT)
input_details = interpreter.get_input_details()
input_shape = input_details[0]['shape']
input_dtype = input_details[0]['dtype']

print(f"Model Input Shape: {input_shape}")
print(f"Model Input Type: {input_dtype}")

# Create random dummy data matching the model's requirements
if input_dtype == np.int8:
    input_data = np.random.randint(-128, 127, input_shape, dtype=np.int8)
elif input_dtype == np.uint8:
    input_data = np.random.randint(0, 255, input_shape, dtype=np.uint8)
else:
    input_data = np.random.random_sample(input_shape).astype(np.float32)

# Run Inference Loop
print("\nStarting Warmup...")
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()

print("Running Speed Test (100 frames)...")
start_time = time.time()

for _ in range(100):
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    
end_time = time.time()
total_time = end_time - start_time
fps = 100 / total_time

print(f"\n🚀 RESULTS:")
print(f"Total Time: {total_time:.2f} seconds")
print(f"FPS: {fps:.2f} frames per second")
