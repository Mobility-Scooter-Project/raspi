# video_analysis
* test run
* [x] Desktop

  ![image](https://github.com/Mobility-Scooter-Project/raspi/assets/44049919/1d3e82a4-1a8d-490a-8b6c-0a52fffda3e2)
* [x] Raspberry Pi

  <img width="1105" alt="Screen Shot 2023-06-05 at 5 06 34 PM" src="https://github.com/Mobility-Scooter-Project/raspi/assets/44049919/88ffc821-f309-43e2-87b7-ad11ee20e636">

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
source ~/.bashrc
```
```
conda config --set auto_activate_base false
```
### Setup motion analysis script
```
conda create -n video python=3.7 -y
```
```
conda activate video
```
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
