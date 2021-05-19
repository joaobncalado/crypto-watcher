# crypto-watcher

Simple script that shows up to two crypto candle bar graphs on a 2.13in e-Paper display, also has support for PiSugar2 battery
The script will iterate over a given list of cryptos

![IMG_20210519_235054](https://user-images.githubusercontent.com/12883662/118895158-873b9e00-b8fd-11eb-85e0-d2d9ac01b220.jpg)


# Hardware
1. RaspberryPi Zero WH
2. Waveshare 2.13inch E-Ink display (https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.13inch-e-paper-hat.htm)
3. PiSugar2 battery (https://www.pisugar.com/)

# Getting started
1. Install OS
2. Enable SPI (for WaveShare)
    - sudo raspi-config
    - Interface Options > SPI > Enable
    - reboot
3. Enable I2C (for PiSugar2)
    - Same as 2) but select I2C instead of SPI
    - sudo apt install i2c-tools
4. Install Git
    - sudo apt install git
5. Install python3
    - sudo apt install python3
6. Install pip
    - sudo apt install python3-distutils
    - curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    - sudo python3 get-pip.py
7. Clone project
    - git clone https://github.com/joaobncalado/crypto-watcher.git
8. Install required pip dependencies:
    - sudo apt install python3-dev # required for spidev
    - sudo apt install libjpeg-dev # required for Pillow
    - sudo apt install libopenjp2-7 # required for Pillow
    - sudo apt install libtiff5 # required for Pillow
    - sudo apt install python-pip # required for RPi
    - sudo apt install python3-rpi.gpio # required for RPi
    - sudo apt install libatlas-base-dev # required for numpy
    - sudo pip3 install spidev
    - sudo pip3 install requests
    - sudo pip3 install pytz
    - sudo pip3 install numpy
    - sudo pip3 install Pillow
    - sudo pip3 install RPi
9. python3 main.py [list of crypto to iterate over]:
    - $ python3 main.py btc eth

