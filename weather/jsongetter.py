from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urlencode
from socket import timeout

from jsonresponse import JSONResponse


class JSONGetter:
    def __init__(self, url, params):
        self._params = params
        self._url = url

    def get(self, additional_params, tout=5, attempts=5):
        cur_params = {**additional_params, **self._params}
        url = self._url.format(urlencode(cur_params))

        for attempt in range(attempts):
            try:
                response = urlopen(url, timeout=tout)
            except HTTPError as e:
                if attempt == attempts - 1:
                    return JSONResponse(e.getcode(), None, e)
            except (URLError, timeout) as e:
                if attempt == attempts - 1:
                    return JSONResponse(None, None, e)
            else:
                try:
                    content = response.read().decode('ascii')
                except Exception as e:
                    return JSONResponse(None, None, e)
                else:
                    return JSONResponse(response.getcode(), content, None)
