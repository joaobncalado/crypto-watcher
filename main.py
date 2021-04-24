# TODO: Uncomment the epd_2in13_V2 line and comment the epd_stub one if you want to run it on the display
# from epd_stub import EPD
from epd2in13_V2 import EPD

from PIL import Image, ImageDraw, ImageFont

from typing import List, Tuple, Dict, Callable
import json
import time
import datetime
import pytz
import math
import logging
import requests
import epdconfig
from pisugar2py import PiSugar2

logging.basicConfig(level=logging.DEBUG)

SLEEP_TIME_BETWEEN_REFRESHES = 900

def fetch_ohlc(symbol: str) -> List[Tuple[float, ...]]:
    res = requests.get(
        "https://api.binance.com/api/v3/klines", params={"symbol": symbol.upper(), "interval": "1h", "limit": 25})
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
    draw.rectangle((x, y_transformer(
        max(ohlc[0], ohlc[3])), x + 2, y_transformer(min(ohlc[0], ohlc[3]))), fill=1)
    draw.line(
        (x + 1, y_transformer(ohlc[1]), x + 1, y_transformer(ohlc[2])), fill=1)


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


def main():

    ps = PiSugar2()
    logging.info("PiSugar2 loaded...")
    battery_percentage = ps.get_battery_percentage()
    logging.info("Battery: " + str(int(battery_percentage.value)))
    epd = EPD()
    logging.info("Initiating EPD...")
    epd.init(epd.FULL_UPDATE)
    logging.info("Clearing display...")
    epd.Clear(0xFF)

    logging.info("Starting...")
    img = Image.new("1", (epd.height, epd.width), 255)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 20)
    font_small = ImageFont.truetype("OpenSans-Regular.ttf", 16)
    font_tiny = ImageFont.truetype("OpenSans-Regular.ttf", 12)

    timezone = pytz.timezone("Europe/Lisbon")
    while True:

        draw = ImageDraw.Draw(img)
        draw.rectangle((0, 0, epd.height, epd.width), fill=0)
        
        #BTC
        logging.info("Fetching BTC...")
        price, diff, ohlc = fetch_crypto_data("btcusdt")
        
        draw.text((8, 5), text="BTC {}$".format(
            price_to_str(price)), font=font, fill=1)

        diff_symbol = ""
        if diff > 0:
            diff_symbol = "+"
        if diff < 0:
            diff_symbol = "-"

        draw.text((8, 30), text="{}{}$".format(diff_symbol,
                                               price_to_str(diff)), font=font_small, fill=1)
        
        render_ohlc_data(18, ohlc, draw)
        
        #ETH
        logging.info("Fetching ETH...")
        price, diff, ohlc = fetch_crypto_data("ethusdt")
        
        draw.text((130, 5), text="ETH {}$".format(
            price_to_str(price)), font=font, fill=1)

        diff_symbol = ""
        if diff > 0:
            diff_symbol = "+"
        if diff < 0:
            diff_symbol = "-"

        draw.text((130, 30), text="{}{}$".format(diff_symbol,
                                               price_to_str(diff)), font=font_small, fill=1)
        
        render_ohlc_data(138, ohlc, draw)
        
        #Last update time
        draw.text((6, 106), text=datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S"),
                  font=font_tiny, fill=1)
        draw.text((130, 106), text = "Battery: " + str(int(battery_percentage.value)) + " %", 
                  font=font_tiny, fill=1)

        logging.info("Sending image to display...")
        epd.display(epd.getbuffer(img))
        logging.info("Sleeping for " + str(SLEEP_TIME_BETWEEN_REFRESHES) + " seconds...")
        time.sleep(SLEEP_TIME_BETWEEN_REFRESHES)


try:
    main()


except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epdconfig.module_exit()
    exit()
