import mrequests as requests
from app_keys import OPENWEATHERMAP_KEY

city = 'London'

def fetch_weather():
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_KEY}&units=metric'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            weather_data = response.json()
            response.close()
            print(weather_data)
            return weather_data
        else:
            print("Failed to fetch weather information:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching weather information:", e)
        return []

# Print weather information to serial
def print_weather_information():
    information = fetch_weather()
    weather = information['weather'][0]['main']
    weather_information = information['weather'][0]['description']
    temperature = information['main']['temp']
    humidity = information['main']['humidity']
    #pressure = information['main']['pressure']
    wind = information['wind']['speed']
    print(f"\nLatest Weather Information for: {city}\n")
    print(f"Weather: {weather} with {weather_information}")
    print(f"Temperature: {temperature}C | Humidity: {humidity}% | Wind: {wind}")
    return city + "|" + str(temperature) + "|" + weather_information + "|" + str(humidity) + "|" + str(wind)
