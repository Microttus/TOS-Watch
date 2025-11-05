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


from import_data import retrive_updated_data, DeviceData
from datetime import datetime
from zoneinfo import ZoneInfo
from enum import Enum


class Trend(Enum):
    NONE = ("x", 0x00)
    UP = ("↑", 0x01)
    UP_DOUBLE = ("⇈", 0x02)
    UP_TRIPLE = ("⤊", 0x03)
    DOWN = ("↓", 0x04)
    DOWN_DOUBLE = ("⇊", 0x05)
    DOWN_TRIPLE = ("⤋", 0x06)

    def __init__(self, symbol: str, code: int):
        self.symbol = symbol      # For printing/logging
        self.code = code          # For MAX7219 control

def us_to_eu_value(value: float) -> float:
    return value / 18

def print_updated_data():
    updated_data = retrive_updated_data()
    trend = Trend[updated_data.lastSGTrend]

    print(f"Last update: {updated_data.lastConduitDateTime}, which is {minutes_since_last_update(updated_data.lastConduitDateTime):.0f} minutes ago")

    print(f"Last trend {updated_data.lastSGTrend}, which is {trend.symbol}.")

    print(f"Last SG {updated_data.lastSG.sg}, and in mmol/L {us_to_eu_value(updated_data.lastSG.sg):.1f}.")

def minutes_since_last_update(last_update: str) -> float:
    dt = datetime.fromisoformat(last_update)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=ZoneInfo("Europe/Oslo"))
    now = datetime.now(ZoneInfo("Europe/Oslo"))

    delta = now - dt
    minutes_passed = delta.total_seconds() / 60

    return minutes_passed


if __name__ == "__main__":
    print_updated_data()