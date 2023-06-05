# video_analysis
* test run
* [x] Desktop

  ![image](https://github.com/Mobility-Scooter-Project/raspi/assets/44049919/1d3e82a4-1a8d-490a-8b6c-0a52fffda3e2)
* [x] Raspberry Pi
* put pretrained model in `/model` and change `MODEL_NAME` 

## SETUP
### Install `conda`
```
cd ~/Desktop
```
```
curl -L https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh > install.sh
```
```
chmod +x install.sh
```
```
./install.sh
```
```
rm install.sh
```
```
source ./bashrc
```
```
conda config --set auto_activate_base false
```
### Setup motion analysis script
```
git clone https://github.com/Mobility-Scooter-Project/raspi.git
```
```
cd raspi/video_analysis
```
```
chmod +x setup.sh
```
```
./setup.sh
```
```
conda activate video & python main.py
```
