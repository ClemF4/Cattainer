# Base image which matches the host (Pi) 
FROM python:3.11-slim-bookworm

# Inject official Pi repository to get the latest versions of the required libraries
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -qO - https://archive.raspberrypi.com/debian/raspberrypi.gpg.key | gpg --dearmor -o /usr/share/keyrings/raspberrypi-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/raspberrypi-archive-keyring.gpg] http://archive.raspberrypi.com/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-picamera2 \
    libcamera-ipa \
    libcamera-tools \
    usbutils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libusb-1.0-0 \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Setup working directory
WORKDIR /app

# Install python libraries
COPY requirements.txt .
# Used --break-system-packages to force installation
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# Copy code
COPY . .

# Create data directory
RUN mkdir -p /data

# This cleans up the windows line endings into linux line endings (since development was on windows)
RUN dos2unix startup.sh 
# Make startup script executable
RUN chmod +x startup.sh
# Run the startup script
CMD ["./startup.sh"]