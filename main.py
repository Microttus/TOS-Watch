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
from data_processing import get_selected_data, TrendData
import screen_print

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
    update_screen()

if __name__ == "__main__":
    main()