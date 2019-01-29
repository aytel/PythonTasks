"""Simple weather informer with info from openweathermap.org.

If you want to get weather by id, launch this file with arguments 'id <id>'.
If you want to get weather by city, launch this file with arguments 'city <cityname with spaces>'.
"""

import argparse
import configparser

from lazyloader import LazyLoader
from weatherstore import WeatherStore
from weathergetter import WeatherGetter
from citygetter import CityGetter


def init_arg_parser():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--city', action='store', dest='city', help='City name')
    arg_parser.add_argument('--id', action='store', dest='id', help='City id')
    return arg_parser


if __name__ == '__main__':
    arg_parser = init_arg_parser()

    args = arg_parser.parse_args()

    config = configparser.ConfigParser()
    config.read('settings.ini')
    API_KEY = config['DEFAULT']['API_KEY']
    WEATHER_URL = config['DEFAULT']['WEATHER_URL']
    CITIES_LIST_PATH = config['DEFAULT']['CITIES_LIST_PATH']
    CITIES = LazyLoader(CITIES_LIST_PATH)
    CITY_URL = config['DEFAULT']['CITY_URL']

    if args.city is None and args.id is None:
        city_getter = CityGetter(CITY_URL)
        city_response = city_getter.get()
        if city_response.content is not None:
            args.city = city_response.content
        else:
            args.city = 'Yekaterinburg'
            print(f'Can\'t detect your city, hope you\'re from {args.city}')

    weather_getter = WeatherGetter(API_KEY, WEATHER_URL, CITIES)

    if args.city is not None:
        response = weather_getter.get(args.city)
    else:
        response = weather_getter.get(args.id, search_by_id=True)

    if response.content is not None:
        if response.additional is not None:
            print(response.additional)
        weather_store = WeatherStore.get_from_json(response.content)
        print(weather_store)
    else:
        print(response.error)
