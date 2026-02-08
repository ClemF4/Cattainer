# 1. Base Image: Match Host (Debian Bookworm)
FROM python:3.11-slim-bookworm

# 2. Install System Dependencies
# We need 'usbutils' and 'libgl' for OpenCV/Coral
RUN apt-get update && apt-get install -y \
    curl \
    usbutils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libusb-1.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 3. Setup Work Directory
WORKDIR /app

# 4. Install Python Libraries
COPY requirements.txt .
# We use --break-system-packages to force installation
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# 5. Copy Code
COPY . .

# 6. Create data directory
RUN mkdir -p /data

# 7. Run
CMD ["python", "cattainer.py"]