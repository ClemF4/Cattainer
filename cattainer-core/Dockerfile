#Have the base image be a modern debian version, not lightweight so that it comes with wget preinstalled
FROM python:3.11-bookworm

#Create the folder for this application
WORKDIR /usr/local/app

#Set the path to the device's global package repository
ENV PYTHONPATH=/usr/lib/python3/dist-packages

COPY requirements.txt .

#Install requirements.txt & perform all the commands in my setup.sh script https://docs.docker.com/reference/dockerfile/#run
RUN <<EOF
#Add raspberry pis repository to debians source list
apt-get update && apt-get install -y gnupg
apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E
echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list
apt-get update

#Install requirements.txt
pip install --no-cache-dir -r requirements.txt
apt-get update

#Install cv2 graphics library & picamera2
apt-get install -y libgl1 python3-picamera2

#Install the TPU drivers
wget https://github.com/feranick/libedgetpu/releases/download/16.0TF2.19.1-1/libedgetpu-dev_16.0tf2.19.1-1.bookworm_arm64.deb
dpkg -i libedgetpu-dev_16.0tf2.19.1-1.bookworm_arm64.deb
apt-get install -f -y 
rm libedgetpu-dev_16.0tf2.19.1-1.bookworm_arm64.deb
EOF

#Copy source files into this new working directory
COPY . . 

#Setup an app user so the container doesn't run as the root user
RUN useradd app
#Add the app user to the video & plugdev groups to give app user perms to access TPU & camera
RUN usermod -aG video app && usermod -aG plugdev app && usermod -aG gpio app
USER app

CMD ["python", "cattainer.py"]
