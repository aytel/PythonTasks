"""Simple weather informer with info from openweathermap.org.

If you want to get weather by id, launch this file with arguments 'id <id>'.
If you want to get weather by city, launch this file with arguments 'city <cityname with spaces>'.
"""

import sys
import json
import argparse
import configparser
from urllib.request import urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError


def load_cities():
    global CITIES
    with open(CITIES_LIST_PATH, "r", encoding="utf8") as file:
        CITIES = json.load(file)
        file.close()


def levenstein(str1, str2):
    """
    :return Levenstein distance between str1 and str2.
    """

    n, m = len(str1), len(str2)
    dp = [[0 for _ in range(m + 1)] for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = min(
                dp[i][j - 1] + 1,
                dp[i - 1][j] + 1,
                dp[i - 1][j - 1] + (str1[i - 1] != str2[j - 1])
            )

    return dp[n][m]


def get_json(mode, city):
    """
        :param mode - 0 if we search by id and 1 if by city
        :param city - string with id or city name
        :return json info about city
    """

    mode = 'q' if mode == 1 else 'id'
    params = urlencode({mode: str(city), 'units': 'metric', 'appid': API_KEY})

    try:
        params = urlencode({mode: str(city), 'units': 'metric', 'appid': API_KEY})
        response = urlopen(WEATHER_URL.format(params))
    except HTTPError:
        if mode == 'id':
            print('Unknown id, try again')
            sys.exit(0)
        else:
            load_cities()
            cur, min_dist = None, 10 ** 9
            for candname in (map(lambda x: x["name"], CITIES)):
                val = levenstein(city.lower(), candname.lower())
                if val < min_dist:
                    cur, min_dist = candname, val
            print(f'Unknown city, best match is {cur}, printing result for it')

            params = urlencode({mode: str(cur), 'units': 'metric', 'appid': API_KEY})
            response = urlopen(WEATHER_URL.format(params))

    data = response.read().decode('ascii')
    return data


def printweather(data):
    """
    Prints temperature and cloudiness of given city.

    :param data - json string with info
    """
    dataenc = json.loads(data)

    main = dataenc["main"]
    temp = main["temp"]
    clouds = dataenc["clouds"]["all"]
    print(f"County is {dataenc['sys']['country']}")
    print(f"City is {dataenc['name']}")
    print(f"Temperature is {temp}°C")
    print(f"Cloudiness is {clouds}%")


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--city', action='store', dest='city', help='City name')
    arg_parser.add_argument('--id', action='store', dest='id', help='City id')

    args = arg_parser.parse_args()

    if args.city is None and args.id is None:
        print('Unknown mode, try again')
        sys.exit(0)

    config = configparser.ConfigParser()
    config.read('settings.ini')
    API_KEY = config['DEFAULT']['API_KEY']
    WEATHER_URL = config['DEFAULT']['WEATHER_URL']
    CITIES_LIST_PATH = config['DEFAULT']['CITIES_LIST_PATH']

    if args.city is not None:
        data = get_json(1, args.city)
    else:
        data = get_json(0, args.id)
    printweather(data)
