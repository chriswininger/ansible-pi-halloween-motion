Ansible Pi Halloween Motion
===========================

This is a project to configure a rasperry pi to turn heads, literally by using motion tracking to rotate baby doll
heads or other objects.

This project takes inspiration from [this great video](https://youtu.be/7m1dUC_UUts?si=urIwgGufX9uFYnqz).The original
git repo is [here](https://github.com/curiousinventor/skellington)

![halloween-collage.png](pictures%2Fhalloween-collage.png)

## Parts

* PI 4 Model B 8 GB Ram
* Official Raspberry Pi Adapter
* Raspberry Pi NoIR Camera V2
* [https://www.adafruit.com/product/3416](https://www.adafruit.com/product/3416)
* 3 x [Micro Server - High Power/Torque](https://www.adafruit.com/product/2307)
* [5V 2A (2000mA) switching power supply](https://www.adafruit.com/product/276)

## Initial Setup

The ansible scripts assumes that the pi has already been loaded with Rasbian and configured
with ssh access running on port 1027 with user chris.

### Important

You must go into Preferences->Raspberry Pi Configuration under the start menu

Then on the "Interfaces" tab, enable I2C

(this is also where you enable ssh)

I installed the Raspberry Pi OS (64 Bit) base image, released 2023-10-10 using the rpi-imager

### Super Confusing Part

`libcamera-hello` command was working, then to debug `cv2-test.py` I tried running `sudo raspi-config nonint do_legacy 0`,
this seemed to get me in a state where the desktop would not boot, but I could ssh in.

I eventually ran `sudo raspi-config nonint do_legacy 1` out of desperation, now the desktop boots, libcamera-hello fails
but `cv2-test.py` works :shrug:

The boot/config.txt has `start_x=1` though not sure this even matters

### SSH Setup

* Add SSH Keys and Remove Password Access**
  * This is so easy now! From the client issue: `ssh-copy-id <USERNAME>@<IP-OF-PI>`
  * Now we can turn off password login (install vim)
  * `sudo vim /etc/ssh/sshd_config`
  * Look for the following and set:
      ```
      PasswordAuthentication no
      UsePAM no
      Port 1027
      ```
  * sudo nano /etc/ssh/ssh_config
      * Make same changes as above (shrug)
      ```
      PasswordAuthentication no
      UsePAM no
      Port 1027
      ```

  * `sudo systemctl restart sshd`
  * exit and try to ssh back in with a password `ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no -p 1027 chris@192.168.1.8`

### Running the Ansible
 
```
cd ./ansible
ansible-playbook -K ./playbook.yml
```

when prompted enter the sudo password for the pi

## Notes:
* [Camera Installation Instructions](https://www.raspberrypi.com/documentation/accessories/camera.html)
* [Pi Camera2 Python Library](https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf)