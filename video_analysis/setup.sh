sudo apt update
sudo apt install python3-opencv -y  
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh > install.sh
chmod +x install.sh
./install.sh
rm install.sh
conda config --set auto_activate_base false
source ~/.bashrc
conda create -n video python=3.7 -y
conda activate video


