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
from wifi_helper import wait_for_wifi
from screen_print import ScreenPrint

led_screen = ScreenPrint(cascaded=4, block_orientation=-90)

def welcome_message():
    w_msg = "Initiating TOS-Watch"
    logging.info(w_msg)
    led_screen.update_text(w_msg)

def wifi_wait_screen():
    led_screen.wifi_wait_screen(False)
    ip_addr = wait_for_wifi()
    led_screen.confirm_wifi_screen(ip_addr)
    return

def profile_screen() -> bool:
    logging.info("Profiling screen attempting")
    led_screen.wifi_wait_screen(True)
    first_data = get_selected_data()
    if first_data is None:
        logging.warning("Server not available")
        return True
    profile_name = "Welcome: " + first_data.firstName + " " + first_data.lastName
    logging.info(profile_name)
    led_screen.update_text(profile_name)
    return False

def update_screen():
    logging.info("Attempting to update data")
    new_data = get_selected_data()
    if new_data is None:
        logging.warning("Server not available")
        return

    ## Updating screen
    led_screen.update_screen(new_data)

    return

def main():
    welcome_message()
    time.sleep(1)
    wifi_wait_screen()
    time.sleep(3)

    while profile_screen():
        time.sleep(2)

    while True:
        update_screen()
        time.sleep(150)

if __name__ == "__main__":
    main()