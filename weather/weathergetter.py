from jsongetter import JSONGetter


class WeatherGetter:
    def __init__(self, api_key, weather_url, cities=None):
        self._getter = JSONGetter(weather_url, {'units': 'metric', 'appid': api_key})
        self._CITIES = cities

    def get(self, city, search_by_id=False, tout=5, attempts=5):
        if not isinstance(search_by_id, bool):
            raise ValueError("Search_by_id must be bool, programmer is mudak, sry.")

        if search_by_id:
            mode = 'id'
        else:
            mode = 'q'

        response = self._getter.get({mode: city}, tout, attempts)

        if response.code == 404 and self._CITIES is not None:
            city = self._CITIES.get_closest(city)
            response = self._getter.get({mode: city}, tout, attempts)
            response.additional = f'Unknown city, best match is {city}, printing result for it'
            return response
        else:
            return response
