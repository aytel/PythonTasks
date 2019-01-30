from urllib.error import HTTPError
from urllib.error import URLError
from urllib.request import urlopen
from urllib.parse import urlencode
from socket import timeout

from jsonresponse import JSONResponse


class JSONHandler:
    def __init__(self, url):
        self._url = url

    def get(self, params, tout=5, attempts=5, data=None):
        url = self._url.format(urlencode(params))

        for attempt in range(attempts):
            try:
                response = urlopen(url, timeout=tout, data=data)
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

    def send(self, params, data: dict, tout=5, attempts=5):
        return self.get(params, tout, attempts, urlencode(data).encode('utf-8'))
