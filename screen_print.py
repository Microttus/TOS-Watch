import logging
import time

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.legacy import text, show_message
from luma.core.render import canvas
from PIL import ImageFont
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT

from data_processing import TrendData
from trend_symbols import TREND_SYMBOLS



class ScreenPrint(object):

    def __init__(self, port=0, device=0, cascaded=1, block_orientation=0) -> None:
        self.serial = spi(port=port, device=device, gpio=noop())
        self.device = max7219(self.serial, cascaded=cascaded, block_orientation=block_orientation)


    def update_text(self, msg : str) -> None:
        show_message(self.device, msg, fill="white", font=proportional(CP437_FONT))

    def wifi_wait_screen(self) -> None:
        with canvas(self.device) as draw:
            for x,y in TREND_SYMBOLS.get("NO_WIFI", []):
                draw.point((x, y), fill="white")

    def confirm_wifi_screen(self, unit_ip : str) -> None:
        show_message(self.device, unit_ip, fill="white", font=proportional(CP437_FONT))

    def update_screen(self, last_trend : TrendData) -> None:
        if last_trend is None:
            logging.warning(f"Last Trend was empty!")
            return

        if last_trend.minutes_since_last_update < 10:
            self.write_to_screen(last_trend)
        elif 10 < last_trend.minutes_since_last_update < 30:
            last_trend.lastSGTrend = "CLOCK"
            self.write_to_screen(last_trend)
        elif 30 < last_trend.minutes_since_last_update < 120:
            last_trend.lastSGTrend = "CLOCK"
            last_trend.lastSGTrend = " "
            self.write_to_screen(last_trend)
        else:
            last_trend.lastSGTrend = " "
            last_trend.lastSGTrend = " "
            self.write_to_screen(last_trend)


    def write_to_screen(self, last_trend : TrendData) -> None:
        if last_trend is None:
            logging.warning(f"Last Trend was empty!")
            return

        x_coord = 8
        if last_trend.lastSG >= 10.0:
            x_coord += 6

        with canvas(self.device) as draw:
            text(draw, (x_coord,0), str(round(last_trend.lastSG,1)), fill="white", font=proportional(SINCLAIR_FONT))
            for x,y in TREND_SYMBOLS.get(last_trend.lastSGTrend, []):
                draw.point((x, y), fill="white")



if __name__ == "__main__":
    logging.info("Cannot be called as main")
