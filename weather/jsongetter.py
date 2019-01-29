from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urlencode
from socket import timeout

from jsonresponse import JSONResponse


class JSONGetter:
    def __init__(self, API_KEY, WEATHER_URL, CITIES=None):
        self._params = {'units': 'metric', 'appid': API_KEY}
        self._WEATHER_URL = WEATHER_URL
        self._CITIES = CITIES

    def get(self, city, search_by_id=False, tout=5, attempts=5):
        if not isinstance(search_by_id, bool):
            raise ValueError("Search_by_id must be bool, programmer is mudak, sry.")

        if search_by_id:
            mode = 'id'
        else:
            mode = 'q'

        cur_params = {mode: city, **self._params}
        url = self._WEATHER_URL.format(urlencode(cur_params))

        for attempt in range(attempts):
            try:
                response = urlopen(url, timeout=tout)
            except HTTPError as e:
                if attempt == attempts - 1:
                    if e.getcode() == 404 and self._CITIES is not None:
                        city = self._CITIES.get_closest(city)
                        response = self.get(city, search_by_id, tout, attempts)
                        response.new_city = city
                        return response
                    return JSONResponse(None, None, e)
            except (URLError, timeout) as e:
                if attempt == attempts - 1:
                    return JSONResponse(None, None, e)
            else:
                return JSONResponse(response.getcode(), response.read().decode('ascii'), None)
