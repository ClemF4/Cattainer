# Base image which matches the host (Pi) 
FROM python:3.11-slim-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
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