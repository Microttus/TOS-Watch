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
from dataclasses import dataclass

## Data classes

@dataclass
class TrendData:
    minutes_since_last_update: float
    lastSGTrend: str
    lastSG: float
    firstName: str
    lastName: str


## Functions

def us_to_eu_value(value: float) -> float:
    return value / 18


def print_updated_data():
    updated_data = retrive_updated_data()
    if updated_data is None:
        print("Server not available")
        return None
    trend = Trend[updated_data.lastSGTrend]

    print(f"Last update: {updated_data.lastConduitDateTime}, which is {minutes_since_last_update(updated_data.lastConduitDateTime):.0f} minutes ago")

    print(f"Last trend {updated_data.lastSGTrend}, which is {trend.symbol}.")

    print(f"Last SG {updated_data.lastSG.sg}, and in mmol/L {us_to_eu_value(updated_data.lastSG.sg):.1f}.")


def get_selected_data() -> TrendData | None:
    updated_data = retrive_updated_data()
    if updated_data is None:
        return None

    trend = Trend[updated_data.lastSGTrend]
    current_trend = TrendData(
        minutes_since_last_update=minutes_since_last_update(updated_data.lastConduitDateTime),
        lastSG=us_to_eu_value(updated_data.lastSG.sg),
        firstName=updated_data.firstName,
        lastName=updated_data.lastName,
        lastSGTrend=updated_data.lastSGTrend,
    )
    return current_trend


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