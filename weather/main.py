import sys
import urllib.request
import json
import urllib.error

API_KEY = 'be01cef635cf71b292eee67044cb51e3'


def getjson(cityid, API_KEY):
    response = urllib.request.urlopen(
        "https://api.openweathermap.org/data/2.5/weather?id={}"
        "&units=metric"
        "&appid={}".format(cityid, API_KEY)
    )
    data = response.read().decode('ascii')
    return data


def printweather(data):
    dataenc = json.loads(data)

    main = dataenc["main"]
    temp = main["temp"]
    clouds = dataenc["clouds"]["all"]
    print("Temperature is {}°C".format(temp))
    print("Cloudiness is {}%".format(clouds))


if __name__ == '__main__':
    cityid = sys.argv[1]
    data = getjson(cityid, API_KEY)
    printweather(data)
    # print(data)
