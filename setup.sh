# Use this in case i cant get the container to download the TPU drivers

echo "Setting up Coral TPU drivers for Cattainer!"
echo "Only works for Raspberry Pi 5 (Bookworm 64bit)"

wget https://github.com/feranick/libedgetpu/releases/download/16.0TF2.19.1-1/libedgetpu-dev_16.0tf2.19.1-1.bookworm_arm64.deb
echo "Installing the driver..."

sudo dpkg -i libedgetpu-dev_16.0tf2.19.1-1.bookworm_arm64.deb

#this fixes any missing dependancies
sudo apt-get install -f -y

rm libedgetpu-dev_16.0tf2.19.1-1.bookworm_arm64.deb

echo "Hardware drivers are now installed"
