"""Simple weather informer with info from openweathermap.org.

If you want to get weather by id, launch this file with arguments 'id <id>'.
If you want to get weather by city, launch this file with arguments 'city <cityname with spaces>'.
"""

import sys
import urllib.request
import json
import urllib.error

API_KEY = 'be01cef635cf71b292eee67044cb51e3'


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


def getjson(mode, city):
    """
        :param mode - 0 if we search by id and 1 if by city
        :param city - string with id or city name
        :return json info about city
    """

    mode = 'q' if mode == 1 else 'id'
    response = None
    try:
        response = urllib.request.urlopen(
            "https://api.openweathermap.org/data/2.5/weather?{}={}"
            "&units=metric"
            "&appid={}".format(mode, city, API_KEY)
        )
    except urllib.error.HTTPError:
        if mode == 'id':
            print('unknown id, try again')
        else:
            CITIES = json.load(open("./data/city.list.min.json", "r", encoding="utf8"))
            cur, mn = None, 10**9
            for cand in CITIES:
                candname = cand["name"]
                val = levenstein(city.lower(), candname.lower())
                if (val < mn):
                    cur, mn = candname, val
            print('unknown city, best match is {}, printing result for it'.format(cur))

            city = cur

            response = urllib.request.urlopen(
                "https://api.openweathermap.org/data/2.5/weather?{}={}"
                "&units=metric"
                "&appid={}".format(mode, city, API_KEY)
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
    print("County is {}".format(dataenc["sys"]["country"]))
    print("City is {}".format(dataenc["name"]))
    print("Temperature is {}°C".format(temp))
    print("Cloudiness is {}%".format(clouds))


if __name__ == '__main__':
    if sys.argv[1] == 'id':
        cityid = sys.argv[2]
        data = getjson(0, cityid)
    elif sys.argv[1] == 'city':
        city = ' '.join(sys.argv[2:])
        data = getjson(1, city)
    else:
        print('unknown mode')
        exit(0)
    printweather(data)
