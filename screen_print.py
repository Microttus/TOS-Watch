import logging
import time

import trend_symbols

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.render import canvas
from PIL import ImageFont
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

from data_processing import TrendData
from main import update_screen
from trend_symbols import TREND_SYMBOLS



def define_screen():

    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90)


def update_text(msg : str) -> None:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90)
    show_message(device, msg, fill="white", font=proportional(CP437_FONT))

def update_screen(last_trend : TrendData) -> None:
    if last_trend is None:
        logging.warning(f"Last Trend was empty!")
        return

    if last_trend.minutes_since_last_update < 10:
        write_to_screen(last_trend)
    elif 10 < last_trend.minutes_since_last_update < 30:
        last_trend.lastSGTrend = "CLOCK"
        write_to_screen(last_trend)
    elif 30 < last_trend.minutes_since_last_update < 120:
        last_trend.lastSGTrend = "CLOCK"
        last_trend.lastSGTrend = " "
        write_to_screen(last_trend)
    else:
        last_trend.lastSGTrend = " "
        last_trend.lastSGTrend = " "
        write_to_screen(last_trend)


def write_to_screen(last_trend : TrendData) -> None:
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=-90)
    if last_trend is None:
        logging.warning(f"Last Trend was empty!")
        return

    with canvas(device) as draw:
        text(draw, (8,0), str(last_trend.lastSG), fill="white", font=proportional(SINCLAIR_FONT))
        for x,y in TREND_SYMBOLS.get(last_trend.lastSGTrend, []):
            draw.point((x, y), fill="white")



if __name__ == "__main__":
    logging.info("Cannot be called as main")
