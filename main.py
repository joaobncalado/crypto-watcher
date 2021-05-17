#!/usr/bin/python3
# TODO: Uncomment the epd_2in13_V2 line and comment the epd_stub one if you want to run it on the display
from epd_stub import EPD
#from epd2in13_V2 import EPD
from PIL import Image, ImageDraw, ImageFont
from pisugar2py import PiSugar2
from typing import List, Tuple, Dict, Callable

import sys
import json
import time
import datetime
import pytz
import math
import logging
import requests
import epdconfig

logging.basicConfig(level=logging.DEBUG)

SLEEP_TIME_BETWEEN_REFRESHES = 10
RUN_ONCE = False
INVERTED_COLORS = False

def fetch_ohlc(symbol: str) -> List[Tuple[float, ...]]:
    res = requests.get("https://api.binance.com/api/v3/klines",
                       params={"symbol": symbol.upper(), "interval": "1h", "limit": 25})
    res.raise_for_status()

    json_data = json.loads(res.text)

    ohlc = []
    for data_entry in json_data:
        ohlc.append(tuple([float(data_entry[i]) for i in [1, 2, 3, 4]]))

    return ohlc


def fetch_crypto_data(symbol: str) -> Tuple[float, float, List[Tuple[float, ...]]]:
    ohlc_data = fetch_ohlc(symbol)
    price_current = ohlc_data[-1][-1]
    price_day_ago = ohlc_data[0][0]
    price_diff = price_current - price_day_ago

    return price_current, price_diff, ohlc_data


def render_candlestick(ohlc: Tuple[float, ...], x: int, y_transformer: Callable[[float], int], draw: ImageDraw):
    # empty rectangle to represent negative candle sticks
    fill_rectangle = 0 if ohlc[3] < ohlc[0] else 1
    positive_filling = get_color(1)
    draw.line((x + 1, y_transformer(ohlc[1]),
              x + 1, y_transformer(ohlc[2])), fill=positive_filling)
    draw.rectangle((x, y_transformer(max(ohlc[0], ohlc[3])), x + 2, y_transformer(
        min(ohlc[0], ohlc[3]))), fill=get_color(fill_rectangle), outline=positive_filling)


def render_ohlc_data(xPos: int, ohlc: List[Tuple[float, ...]], draw: ImageDraw):
    X_START = xPos
    Y_START = 54
    HEIGHT = 50

    y_min = min([d[2] for d in ohlc])
    y_max = max([d[1] for d in ohlc])

    def y_transformer(y: float) -> int:
        multiplier = HEIGHT / (y_max - y_min)
        offset = int(multiplier * (y - y_min))
        return Y_START + HEIGHT - offset

    x = X_START + 24 * 4 + 1
    for candle_data in ohlc[::-1]:
        x -= 4
        render_candlestick(candle_data, x, y_transformer, draw)


def price_to_str(price: float) -> str:
    exp10 = math.floor(math.log10(abs(price)))
    num_decimals = int(min(5, max(0, 3 - exp10)))
    return "%.*f" % (num_decimals, price)

def get_color(should_fill: int) -> int:
    if INVERTED_COLORS:
        fill_color = should_fill
    else:
        fill_color = 0 if should_fill == 1 else 1
    return fill_color

def main():

    try:
        logging.info("Running for: " + str(len(sys.argv) - 1) +
                     " cryptocurrencies")
        try:
            logging.info("Initializing PiSugar2...")
            ps = PiSugar2()
            logging.info("Getting battery level...")
            battery_percentage = ps.get_battery_percentage()
            logging.info(
                "Battery: " + str(int(battery_percentage.value)) + " %")
            logging.info("Syncing RTC...")
            ps.set_pi_from_rtc()
        except IOError as e:
            logging.info(e)
            ps = False

        logging.info("Initiating EPD...")
        epd = EPD()
        epd.init(epd.FULL_UPDATE)
        logging.info("Clearing display...")
        epd.Clear(0xFF)

        logging.info("Starting...")
        img = Image.new("1", (epd.height, epd.width), 255)

        logging.info("Loading font...")
        font_path_location = "/home/pi/projects/crypto-watcher/OpenSans-Regular.ttf"
        font = ImageFont.truetype(font_path_location, 20)
        font_small = ImageFont.truetype(font_path_location, 16)
        font_tiny = ImageFont.truetype(font_path_location, 12)

        timezone = pytz.timezone("Europe/Lisbon")

        positive_filling = get_color(1)
        negative_filling = get_color(0)

        while True:

            # Iterate the cryptos provided
            for i in range(1, len(sys.argv)):

                crypto_name = sys.argv[i].upper()
                logging.info("Fetching " + crypto_name + "...")
                price, diff, ohlc = fetch_crypto_data(crypto_name + "USDT")

                diff_symbol = ""
                if diff > 0:
                    diff_symbol = "+"
                if diff < 0:
                    diff_symbol = "-"

                # Odds on the left, evens on the right
                if(i % 2):
                    # Left side of the display
                    draw = ImageDraw.Draw(img)
                    draw.rectangle((0, 0, epd.height, epd.width), fill=negative_filling)

                    # Last update time
                    draw.text((6, 106), text=datetime.datetime.now(timezone).strftime(
                        "%Y-%m-%d %H:%M:%S"), font=font_tiny, fill=positive_filling)

                    # Battery percentage
                    if ps != False:
                        # new PiSugar model uses battery_power_plugged & battery_allow_charging to detect real charging status
                        battery_display_text = "Battery: " + \
                            str(int(battery_percentage.value)) + " %"
                        if ps.get_battery_led_amount().value == 2:
                            if ps.get_battery_power_plugged().value and ps.get_battery_allow_charging().value:
                                logging.info("Charging...")
                                battery_display_text = battery_display_text + " CHG"
                        draw.text((130, 106), text=battery_display_text,
                                font=font_tiny, fill=positive_filling)
                    logging.info("Left crypto...")
                    draw.text((8, 5), text="{crypto_name} {value}$".format(
                        crypto_name=crypto_name, value=price_to_str(price)), font=font, fill=positive_filling)
                    draw.text((8, 30), text="{diff_symbol}{diff_value}$".format(
                        diff_symbol=diff_symbol, diff_value=price_to_str(diff)), font=font_small, fill=positive_filling)
                    render_ohlc_data(18, ohlc, draw)
                else:
                    # Right side of the display
                    logging.info("Right crypto...")
                    draw.text((130, 5), "{crypto_name} {value}$".format(
                        crypto_name=crypto_name, value=price_to_str(price)), font=font, fill=positive_filling)
                    draw.text((130, 30), text="{diff_symbol}{diff_value}$".format(
                        diff_symbol=diff_symbol, diff_value=price_to_str(diff)), font=font_small, fill=positive_filling)
                    render_ohlc_data(138, ohlc, draw)
                    if(i == len(sys.argv)):
                        # if its the last crypto of the list the script will send the image
                        # to the display and sleep, out of the loop, no need to do it here
                        break
                    else:
                        # Send image to display and wait SLEEP_TIME_BETWEEN_REFRESHES seconds before continue iterating
                        logging.info("Sending image to display...")
                        epd.init(epd.PART_UPDATE)
                        epd.displayPartial(epd.getbuffer(img))
                        logging.info("Sleeping for " +
                             str(SLEEP_TIME_BETWEEN_REFRESHES) + " seconds...")
                        time.sleep(SLEEP_TIME_BETWEEN_REFRESHES)
            
            # Send image to display
            logging.info("Sending image to display...")
            epd.init(epd.PART_UPDATE)
            epd.displayPartial(epd.getbuffer(img))

            if RUN_ONCE:
                logging.info("Ran once, exiting...")
                exit()
            else:
                logging.info("Sleeping for " +
                             str(SLEEP_TIME_BETWEEN_REFRESHES) + " seconds...")
                time.sleep(SLEEP_TIME_BETWEEN_REFRESHES)

    except IOError as e:
        logging.info(e)

    except KeyboardInterrupt:
        logging.info("Detected ctrl + c:")
        try:
            epdconfig.module_exit()
        except RuntimeError as re:
            logging.error("Error exiting display module:")
            logging.error(re)
        exit()


if __name__ == "__main__":
    main()
