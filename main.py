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

from data_processing import get_selected_data, TrendData

def welcome_message():
    print("Welcome to the TOS-Watch")

def update_screen():
    print("Updating data")

def main():
    welcome_message()
    update_screen()

if __name__ == "__main__":
    main()