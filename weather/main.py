"""Simple weather informer with info from openweathermap.org.

If you want to get weather by id, launch this file with arguments 'id <id>'.
If you want to get weather by city, launch this file with arguments 'city <cityname with spaces>'.
"""

import sys
import json
import argparse
import configparser
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import urlencode
from utils import levenstein
from lazyloader import LazyLoader
from weatherstore import WeatherStore


def get_json(city, mode=False):
    """
        :param mode - 0 if we search by id and 1 if by city
        :param city - string with id or city name
        :return json info about city
    """

    if not isinstance(mode, bool):
        raise ValueError('Mode must be bool, programmer is mudak, sry')
        sys.exit(0)

    if not mode:
        mode = 'q'
    else:
        mode = 'id'

    try:
        params = urlencode({mode: city, 'units': 'metric', 'appid': API_KEY})
        response = urlopen(WEATHER_URL.format(params))
    except HTTPError:
        if mode == 'id':
            print('Unknown id, try again')
            sys.exit(0)
        else:
            cur, min_dist = None, float('inf')
            for candname in map(lambda x: x["name"], CITIES.content):
                val = levenstein(city.lower(), candname.lower())
                if val < min_dist:
                    cur, min_dist = candname, val
            print(f'Unknown city, best match is {cur}, printing result for it')

            params = urlencode({mode: cur, 'units': 'metric', 'appid': API_KEY})
            response = urlopen(WEATHER_URL.format(params))

    data = response.read().decode('ascii')
    return data


def init_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--city', action='store', dest='city', help='City name')
    arg_parser.add_argument('--id', action='store', dest='id', help='City id')
    return arg_parser


if __name__ == '__main__':
    arg_parser = init_arg_parser()

    args = arg_parser.parse_args()

    if args.city is None and args.id is None:
        print('Unknown mode, try again')
        sys.exit(0)

    config = configparser.ConfigParser()
    config.read('settings.ini')
    API_KEY = config['DEFAULT']['API_KEY']
    WEATHER_URL = config['DEFAULT']['WEATHER_URL']
    CITIES_LIST_PATH = config['DEFAULT']['CITIES_LIST_PATH']
    CITIES = LazyLoader(CITIES_LIST_PATH)

    if args.city is not None:
        data = get_json(args.city)
    else:
        data = get_json(args.id, mode=True)

    weather_store = WeatherStore.get_from_json(data)

    print(weather_store)
