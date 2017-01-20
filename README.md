# clicker
TV monitoring and control over RS-232 using Raspberry Pi + USB Serial Adapter

## WORK IN PROGRESS

## RPi Setup Steps
Install requirements:
```bash
sudo apt-get update
sudo apt-get -y install python-pip
sudo apt-get -y install python-serial
sudo pip install paho-mqtt
```
Add udev rule:
Connect USB Serial Adapter and run udev_pair script with sudo:
```bash
sudo python udev_pair.py
```
Test udev rule:
Disconnect and reconnect USB Serial Adapter and run:
```bash
ls -l /dev/usb_serial
```
output should be:
```bash
lrwxrwxrwx 1 root root 7 Jan 20 00:25 /dev/usb_serial -> ttyUSB0
```
Now, regardless of USB port the adapter is connected to, or any other USB devices connected to the RPi, the USB Serial Adapter will have the persistent name: '/dev/usb_serial'