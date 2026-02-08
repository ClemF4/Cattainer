# 1. Base Image: Debian 12 (Bookworm) with Python 3.11
# This matches your Host OS exactly.
FROM python:3.11-slim-bookworm

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install System Dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    usbutils \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# 4. Install the Google Coral Driver (libedgetpu1-std)
# We use the standard Google repo, which hosts the v16 driver you have.
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor -o /usr/share/keyrings/coral-edgetpu-archive-keyring.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/coral-edgetpu-archive-keyring.gpg] https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list \
    && apt-get update && apt-get install -y \
    libedgetpu1-std \
    && rm -rf /var/lib/apt/lists/*

# 5. Setup Work Directory
WORKDIR /app

# 6. Install Python Libraries
COPY requirements.txt .
# CRITICAL: We use --break-system-packages because we are overriding 
# the system's python environment to ensure version 2.14.0 is used.
RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

# 7. Copy Code
COPY . .

# 8. Create data directory
RUN mkdir -p /data

# 9. Run
CMD ["python", "cattainer.py"]