"""Simple weather informer with info from openweathermap.org.

If you want to get weather by id, launch this file with arguments 'id <id>'.
If you want to get weather by city, launch this file with arguments 'city <cityname with spaces>'.
"""

import sys
import urllib.request
import json
import urllib.error
import argparse
import configparser


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
    response = None
    try:
        response = urllib.request.urlopen(
            WEATHER_URL.format(mode, city, API_KEY)
        )
    except urllib.error.HTTPError:
        if mode == 'id':
            print('unknown id, try again')
        else:
            CITIES = json.load(open(CITIES_LIST_PATH, "r", encoding="utf8"))
            cur, mn = None, 10 ** 9
            for cand in CITIES:
                candname = cand["name"]
                val = levenstein(city.lower(), candname.lower())
                if val < mn:
                    cur, mn = candname, val
            print(f'unknown city, best match is {cur}, printing result for it')

            city = cur

            response = urllib.request.urlopen(
                WEATHER_URL.format(mode, city, API_KEY)
            )

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
