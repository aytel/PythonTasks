import json


class WeatherStore:
    def __init__(self, country, city, temp, clouds):
        self.country = country
        self.city = city
        self.temp = temp
        self.clouds = clouds

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
