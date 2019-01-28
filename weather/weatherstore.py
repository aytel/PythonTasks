import json
from dataclasses import dataclass


@dataclass
class WeatherStore:
    country: str
    city: str
    temp: float
    clouds: int

    @staticmethod
    def get_from_json(content):
        encoded = json.loads(content)
        main = encoded['main']
        temp = main['temp']
        clouds = encoded['clouds']['all']
        country = encoded['sys']['country']
        city = encoded['name']

        return WeatherStore(country, city, temp, clouds)

    def __str__(self):
        return f"County is {self.country}\n" \
               f"City is {self.city}\n" \
               f"Temperature is {self.temp}°C\n" \
               f"Cloudiness is {self.clouds}%\n"
