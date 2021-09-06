# crypto-watcher

Simple script that shows up to two crypto candle bar graphs on a 2.13in e-Paper display, also has support for PiSugar2 battery
The script will iterate over a given list of cryptos

![IMG_20210519_235054](https://user-images.githubusercontent.com/12883662/118895158-873b9e00-b8fd-11eb-85e0-d2d9ac01b220.jpg)


# Hardware
1. RaspberryPi Zero WH
2. Waveshare 2.13inch E-Ink display
    - https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.13inch-e-paper-hat.htm
    - http://www.waveshare.com/wiki/2.13inch_e-Paper_HAT
3. PiSugar2 battery
    - https://www.pisugar.com/
    - https://github.com/PiSugar/PiSugar/wiki/PiSugar2

# Getting started
1. Install OS
2. Enable SPI (for WaveShare)
    - sudo raspi-config
    - Interface Options > SPI > Enable
    - reboot
3. Enable I2C (for PiSugar2)
    - sudo raspi-config
    - Interface Options > I2C > Enable
    - reboot
    - sudo apt install i2c-tools
4. Install Git
    - sudo apt install git
5. Install python3
    - sudo apt install python3
6. Install pip
    - sudo apt install python3-distutils
    - curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    - sudo python3 get-pip.py
7. Install required pip dependencies:
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
    - sudo pip3 install RPi.GPIO
8. PiSugar2 Software Installation
    - curl http://cdn.pisugar.com/release/Pisugar-power-manager.sh | sudo bash
    - http://<your raspberry ip>:8421
9. Clone project
    - git clone https://github.com/joaobncalado/crypto-watcher.git
    - $ cd crypto-watcher
    - $ sudo nano main.py
        - comment the line:
            from epd_stub import EPD
        - uncomment the line:
            #from epd2in13_V2 import EPD
        - save and exit:
            ctrl+X
            Y

10. python3 main.py [list of crypto to iterate over separated by spaces]:
    - $ python3 main.py btc eth

11. (optional) Configuring PiSugar2 commands:
    - one click: Custom Shell to run the script
        /home/pi/projects/crypto-watcher/main.py btc eth ada xrp bnb vet nano doge
    - double click: shutdown
    - long press: Custom Shell to kill the script
        ps aux | grep python | grep -v "grep" | awk '{print $2}' | sudo xargs kill -9

