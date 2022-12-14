import asyncio
import csv
import os
import aiohttp
import socket
import pandas as pd

from time import sleep
from datetime import datetime
from colorama import Fore
from meteostat import Stations
from api import Forecast

oklahoma = [["Oklahoma", "OK", "40"]]
# State, Abbreviation, FP code
us_states = [
    ["Alabama", "AL", "01"], ["Arizona", "AZ", "04"], ["Arkansas", "AR", "05"], ["California", "CA", "06"],
    ["Colorado", "CO", "08"], ["Connecticut", "CT", "09"], ["Delaware", "DE", "10"], ["Florida", "FL", "12"],
    ["Georgia", "GA", "13"], ["Idaho", "ID", "16"], ["Illinois", "IL", "17"], ["Indiana", "IN", "18"],
    ["Iowa", "IA", "19"], ["Kansas", "KS", "20"], ["Kentucky", "KY", "21"], ["Louisiana", "LA", "22"],
    ["Maine", "ME", "23"], ["Maryland", "MD", "24"], ["Massachusetts", "MA", "25"], ["Michigan", "MI", "26"],
    ["Minnesota", "MN", "27"], ["Mississippi", "MS", "28"], ["Missouri", "MO", "29"], ["Montana", "MT", "30"],
    ["Nebraska", "NE", "31"], ["Nevada", "NV", "32"], ["New Hampshire", "NH", "33"], ["New Jersey", "NJ", "34"],
    ["New Mexico", "NM", "35"], ["New York", "NY", "36"], ["North Carolina", "NC", "37"], ["North Dakota", "ND", "38"],
    ["Ohio", "OH", "39"], ["Oklahoma", "OK", "40"], ["Oregon", "OR", "41"], ["Pennsylvania", "PA", "42"],
    ["Rhode Island", "RI", "44"], ["South Carolina", "SC", "45"], ["South Dakota", "SD", "46"],
    ["Tennessee", "TN", "47"], ["Texas", "TX", "48"], ["Utah", "UT", "49"], ["Vermont", "VT", "50"],
    ["Virginia", "VA", "51"], ["Washington", "WA", "53"], ["West Virginia", "WV", "54"], ["Wisconsin", "WI", "55"],
    ["Wyoming", "WY", "56"],
]


async def main() -> int:
    await asyncio.gather(*map(loop, oklahoma))
    return 0


async def loop(state: list) -> None:
    # main loop for each state
    state_abv = state[1]
    stations = create_df(state_abv)

    task_1 = asyncio.create_task(fetch_data(stations, state_abv))
    await task_1


def create_df(state_abv: str) -> pd.DataFrame:
    # create dataframe with all stations in state using meteostat
    try:
        stations = Stations()
        stations = stations.region('US', state_abv)
        stations = stations.fetch()
        exclude = ['N/A']
        stations = stations[~stations.icao.isin(exclude)]  # exclude invalid stations
        return stations
    except Exception as e:
        print(Fore.RED + f"Error in create_df while working on {state_abv}: {e}")


async def fetch_data(stations: pd.DataFrame, state_abv: str):
    # separate station coordinates from stations, create appropriate dirs in shared vol
    coords = stations[["latitude", "longitude"]]
    day = datetime.today().strftime('%Y-%m-%d')
    hour = datetime.utcnow().isoformat(timespec='hours')
    dir_path = f'/src/data-vol/{str(day)}/{str(hour)}'
    try:
        os.makedirs(dir_path)
    except Exception as e:
        print(f"Could not create {dir_path}: {e}")

    # fetch data from weather.gov api and put in Queue
    stat_data = []
    async with aiohttp.ClientSession(trust_env=True) as session:
        for row, st_id in enumerate(stations["icao"]):
            loc = coords.iloc[row]
            api_req = Forecast(loc, session)
            forecast_url = await api_req.get_json()
            if forecast_url:
                try:
                    await api_req.get_forecast(forecast_url, stat_data)
                    # forecast_args order: temp, windSp, windDir, lat, lon
                except:
                    stat_data.append([None, None, None, loc["latitude"], loc["longitude"]])
            else:
                stat_data.append([None, None, None, loc["latitude"], loc["longitude"]])

    # Write data to csv and save to shared vol
    fn = f"{state_abv}-{hour}.csv"
    with open(rf"/src/data-vol/{day}/{hour}/{fn}", "w", newline="\n") as file:
        fields = ['temp(F)', 'windSp(mph)', 'windDir', 'lat', 'lon']
        write = csv.writer(file)
        write.writerow(fields)
        write.writerows(stat_data)


def connect_to_container(host: str, port: int) -> None:
    # Check that PNG-Mapper is up and running to let it know this container is done
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    for i in range(10):
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Connection to port {port} on {host} established.")
            break
        else:
            print(f"Port {port} on {host} is not responding. Attempt to connect #{i+1}")
            sleep(2)


if __name__ == "__main__":
    asyncio.run(main())
    connect_to_container('png-mapper', 8877)