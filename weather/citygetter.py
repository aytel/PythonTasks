from jsongetter import JSONGetter


class CityGetter:
    def __init__(self, city_url):
        self._getter = JSONGetter(city_url)
        self._CITY_URL = city_url

    def get(self):
        return self._getter.get()
