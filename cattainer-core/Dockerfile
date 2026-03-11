#Have the base image be a modern debian version, not lightweight so that it comes with wget preinstalled
FROM python:3.11-bookworm

#Create the folder for this application
WORKDIR /usr/local/app

#Set the path to the device's global package repository
ENV PYTHONPATH=/usr/lib/python3/dist-packages

COPY requirements.txt .

#Install requirements.txt & perform all the commands in my setup.sh script https://docs.docker.com/reference/dockerfile/#run
RUN <<EOF
#Connect raspberry pis repository to debians source list
apt-get update && apt-get install -y wget gnupg && \
wget -qO - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | gpg --dearmor -o /etc/apt/trusted.gpg.d/raspberrypi-archive-keyring.gpg && \
echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list

#Install requirements.txt
pip install --no-cache-dir -r requirements.txt
apt-get update

#Install cv2 graphics library & picamera2
apt-get install -y libgl1 python3-picamera2 libusb-1.0-0 libudev1

#Install the TPU drivers
wget https://github.com/feranick/libedgetpu/releases/download/16.0TF2.19.1-1/libedgetpu1-std_16.0tf2.19.1-1.bookworm_arm64.deb
dpkg -i libedgetpu1-std_16.0tf2.19.1-1.bookworm_arm64.deb
apt-get install -f -y 
rm libedgetpu1-std_16.0tf2.19.1-1.bookworm_arm64.deb
EOF

#Setup an app user so the container doesn't run as the root user
RUN useradd -m app

#Copy source files into this new working directory & give app user permissions over them
COPY --chown=app:app . .

#Gove the app user the video & plugdev groups to give app user perms to access TPU & camera
RUN usermod -aG video app && usermod -aG plugdev app
USER app

CMD ["python", "core.py"]
