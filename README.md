# Cattainer

## Installation

### Prerequisites: Install Docker & Docker Compose
Cattainer relies on Docker and Docker Compose. Run the following commands one by one in your terminal to install them and grant your user account the correct permissions:

```
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
```
### 1. Download

Head to the releases page & download our release using the command line on the Raspberry Pi.

Use `wget <link to file>` to download the release you want.


### 2. Extract Files
### .zip Files
Use the command `unzip <filename>` to unzip this file and head on to step 

### .tar.gz 
use the command `tar -xzf <filename>.tar.gz` to extract the archive


### 3. Run Containers

Open the folder you just extracted using `cd <foldername>`
Then start the containers using the following command `docker compose up -d`

