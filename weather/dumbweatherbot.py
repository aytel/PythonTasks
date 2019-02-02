import json

from time import sleep

from weathergetter import WeatherGetter
from jsonhandler import JSONHandler
from weatherstore import WeatherStore

class DumbWeatherBot:
    def __init__(self, bot_token, weather_getter: WeatherGetter):
        self._tlg_url = f'https://api.telegram.org/bot{bot_token}/'
        self._weather_getter = weather_getter
        self._upd_getter = JSONHandler(self._tlg_url + 'getUpdates')
        self._msg_sender = JSONHandler(self._tlg_url + 'sendMessage')

    def get_upd(self) -> dict or None:
        response = self._upd_getter.get({})
        if not response.content:
            return None
        else:
            data = json.loads(response.content)
            if not data['ok']:
                return None
            else:
                return data['result']

    def send_msg(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        response = self._msg_sender.send({}, params)
        if not response.content:
            return None
        else:
            data = json.loads(response.content)
            return data

    def handle_msg(self, msg):
        if msg['text'] == '/start':
            text = "Hello! I'm weather bot and I'm dumb.\n" \
                  "Give me a city.\n"
        else:
            weather_response = self._weather_getter.get(msg['text'])

            text = ""

            if weather_response.content is not None:
                if weather_response.additional is not None:
                    text += weather_response.additional + '\n'
                weather_store = WeatherStore.get_from_json(weather_response.content)
                text += str(weather_store)
            else:
                text += str(weather_response.error)

        self.send_msg(msg['chat']['id'], text)

    def work(self):
        last_id = -1
        while True:
            sleep(0.1)
            msgs = self.get_upd()

            if len(msgs) == 0:
                continue

            last_msg = msgs[-1]

            update_id = last_msg['update_id']
            if update_id == last_id:
                continue
            else:
                last_id = update_id
                self.handle_msg(last_msg['message'])
