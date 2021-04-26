# crypto-watcher

Simple script that shows up to two crypto candle bar graphs on a 2.13in e-Paper display, also has support for PiSugar2 battery

![snapshot](https://user-images.githubusercontent.com/12883662/115999283-185f7380-a5e3-11eb-9685-bb80fef58d10.jpg)


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
4. Install Git
    - sudo apt install git
5. Install python3
    - sudo apt install python3
6. Install pip
    - sudo apt install python3-distutils
    - curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    - python3 get-pip.py
7. Clone project
    - git clone https://github.com/joaobncalado/crypto-watcher.git
8. Install required pip dependencies:
    - sudo apt install python3-dev # required for spidev
    - sudo apt install libjpeg-dev # required for Pillow
    - sudo apt-get install python-pip
    - python3 -m pip install spidev==3.5
    - python3 -m pip install requests==2.21.0
    - python3 -m pip install pytz==2021.1
    - python3 -m pip install numpy==1.16.2 # this takes a while (1h+ on rpi0)
    - python3 -m pip install Pillow==8.2.0
    - python3 -m pip install RPi==0.0.1
9. python3 main.py
