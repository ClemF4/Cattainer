#Have the base image be a modern debian version, not lightweight so that it comes with wget preinstalled
FROM python:3.11-bookworm

#Create the folder for this application
WORKDIR /usr/local/app

COPY requirements.txt .

#Install requirements.txt & perform all the commands in my setup.sh script https://docs.docker.com/reference/dockerfile/#run
RUN <<EOF
pip install --no-cache-dir -r requirements.txt
pip uninstall opencv-python -y
apt-get update
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
RUN usermod -aG video app && usermod -aG plugdev app
USER app

CMD ["python", "cattainer.py"]
