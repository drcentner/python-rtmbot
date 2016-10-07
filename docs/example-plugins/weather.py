from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return
import yaml
import urllib2
import json

# Import variables from config file
config = yaml.load(open('plugins/weather.conf', 'r'))

weather_url = config.get('WEATHER_URL')

outputs = []


def get_weather(weather_url):
    f = urllib2.urlopen(weather_url)
    weather_json = f.read()
    f.close()
    w = json.loads(weather_json)

    weather_forecast = str(
    "Location: " + w['current_observation']['display_location']['full'] + "\n" +
    "Station: " + w['current_observation']['station_id'] + "\n" +
    "Current temp: " + w['current_observation']['temperature_string'] + "\n" +
    "Feels like: " + w['current_observation']['feelslike_string'] + "\n" +
    "Relative humidity: " + w['current_observation']['relative_humidity'] + "\n" +
    "Wind: " + w['current_observation']['wind_string'] + "\n" +
    "Weather: " + w['current_observation']['weather'] + "\n"
    )

    return weather_forecast

def process_message(data):
    if data['text'] == 'weather':
        # Get weather and store in a variable
        weather_forecast = get_weather(weather_url)

        # Respond with weather forecast
        outputs.append([data['channel'], weather_forecast])
