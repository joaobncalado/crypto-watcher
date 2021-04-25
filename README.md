# crypto-watcher

Simple script that shows up to two crypto candle bar graphs on a 2.13in e-Paper display, also has support for PiSugar2 battery

![snapshot](https://user-images.githubusercontent.com/12883662/115999283-185f7380-a5e3-11eb-9685-bb80fef58d10.jpg)


# Hardware
1. RaspberryPi Zero WH
2. Waveshare 2.13inch E-Ink display (https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.13inch-e-paper-hat.htm)
3. PiSugar2 battery (https://www.pisugar.com/)

# Getting started
1. Install OS
2. Install python3
3. Install pip
4. Install required pip packages
    - spidev==3.5
    - requests==2.21.0
    - pytz==2021.1
    - numpy==1.16.2
    - Pillow==8.2.0
    - RPi==0.0.1

5. Enable SPI
    - sudo raspi-config
    - Interface Options
    - SPI
    - Enable
    - reboot

6. Clone project
7. python3 main.py
