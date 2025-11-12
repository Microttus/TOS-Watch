#######################################################
#
#                     TOS-Watch
#
#          Pipeline for parsing carelink-clinet
#              data on a max7219 screen
#
#                By: IceCube Solutions
#
#######################################################

import logging
import time
from data_processing import get_selected_data, TrendData
from screen_print import ScreenPrint

led_screen = ScreenPrint(cascaded=4, block_orientation=-90)

def welcome_message():
    w_msg = "Welcome to the TOS-Watch"
    logging.info(w_msg)
    screen_print.update_text(w_msg)


def update_screen():
    logging.info("Attempting to update data")
    new_data = get_selected_data()
    if new_data is None:
        logging.warning("Server not available")
        return

    ## Updating screen
    screen_print.update_screen(new_data)

    return

def main():
    welcome_message()
    time.sleep(1)
    update_screen()
    time.sleep(5)

if __name__ == "__main__":
    main()