# motion sensor
* REU2022 mobility scooter work 
* https://github.com/Mobility-Scooter-Project/NSFREU2022-Mobility-Scooter

* `motion_only.py` records motion data only ~ 30fps

* `video_and_motion.py` records both motion and video at 5fps with only raspberrypi
  
# trouble shooting model B
* the first problem is can't detect sensor_hat

```
 sudo nano /boot/config.txt
```
* in config.txt make sure to have these lines, if its empty or only comments, add the code

```
# Uncomment some or all of these to enable the optional hardware interfaces
#dtparam=i2c_arm=on
#dtparam=i2s=on
#dtparam=spi=on

# Uncomment this to enable the lirc-rpi module
#dtoverlay=lirc-rpi

# Additional overlays and parameters are documented /boot/overlays/README
dtoverlay=rpi-sense
```
* the second problem is Fail to initialise TC34725 colour sensor.(sensor not present), this website teached how to fix it
* [https://forums.raspberrypi.com/viewtopic.php?t=338641](https://github.com/astro-pi/python-sense-hat/issues/125)https://github.com/astro-pi/python-sense-hat/issues/125
  
