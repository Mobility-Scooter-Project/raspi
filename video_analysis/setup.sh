sudo apt update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
source /home/pi/.bashrc
conda create -n video python=3.7 -y
conda activate video
pip install -r requirements.txt
pip install ./assets/mediapipe-0.8-cp37-cp37m-linux_aarch64.whl
pip install protobuf==3.20.*





