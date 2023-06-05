sudo apt update
sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh > install.sh
chmod +x install.sh
./install.sh
rm install.sh
conda config --set auto_activate_base false
source ~/.bashrc
conda create -n video python=3.7 -y
conda activate video
pip install -r requirements.txt
pip install ./assets/mediapipe-0.8-cp37-cp37m-linux_aarch64.whl
pip install protobuf==3.20.*





