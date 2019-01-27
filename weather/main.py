import sys
import urllib.request
import json
import urllib.error

API_KEY = 'be01cef635cf71b292eee67044cb51e3'
#CITIES = json.load(open("./data/city.list.json", "r", encoding="utf8"))


def getjson(mode, city, API_KEY):
    mode = 'q' if mode == 1 else 'id'
    response = urllib.request.urlopen(
        "https://api.openweathermap.org/data/2.5/weather?{}={}"
        "&units=metric"
        "&appid={}".format(mode, city, API_KEY)
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
    if sys.argv[1] == 'id':
        cityid = sys.argv[2]
        data = getjson(0, cityid, API_KEY)
    elif sys.argv[1] == 'city':
        city = ' '.join(sys.argv[2:])
        data = getjson(1, city, API_KEY)
    else:
        print('unknown mode')
        exit(0)
    printweather(data)
