# 1. Base Image: Mirroring your Pi (Debian 12 Bookworm / Python 3.11)
FROM python:3.11-slim-bookworm

# 2. Set environment variables to keep Python clean
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install System Dependencies
# - curl/gnupg: For downloading Google keys
# - usbutils: To verify the Coral stick is connected
# - libgl1/libglib2.0-0: Required dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    usbutils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Install Google Coral EdgeTPU Drivers (Bookworm Compatible)
# Debian 12 deprecated 'apt-key', so we use the signed-by keyring method.
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/coral-edgetpu-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/coral-edgetpu-archive-keyring.gpg] https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list \
    && apt-get update && apt-get install -y \
    libedgetpu1-std \
    && rm -rf /var/lib/apt/lists/*

# 5. Set up the working directory
WORKDIR /app

# 6. Install Python Libraries
COPY requirements.txt .
# We use --break-system-packages because Debian 12 is strict about pip, 
# but inside a container, this is safe and necessary.
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# 7. Copy your application code
COPY . .

# 8. Create a directory for saving the zone configuration
RUN mkdir -p /data

# 9. Define the command to run your app
CMD ["python", "cattainer.py"]