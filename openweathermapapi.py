import mrequests as requests
import re
from app_keys import OPENWEATHERMAP_KEY
from geocodeapi import GetLocationCoordinates

def FetchWeather(city):
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_KEY}&units=metric'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            response.close()
            return weather_data
        else:
            print("Failed to fetch weather information:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching weather information:", e)
        return []

# Print weather information to serial
def PrintWeatherInformation(city):
    location = GetLocationCoordinates(city)
    information = FetchWeather(city)
    weather = information['weather'][0]['main']
    weather_information = information['weather'][0]['description']
    temperature = information['main']['temp']
    humidity = information['main']['humidity']
    #pressure = information['main']['pressure']
    wind = information['wind']['speed']
    city = city.replace("%20", " ")  # Replace %20 with a space
#     print(f"\nLatest Weather Information for: {city}")
#     print(f"Weather: {weather} with {weather_information}")
#     print(f"Temperature: {temperature}C | Humidity: {humidity}% | Wind: {wind}\n")
    return city + "|" + str(temperature) + "|" + weather_information + "|" + str(humidity) + "|" + str(wind) + "|" + location['longt'] + "|" + location['latt']

