import mrequests as requests
from app_keys import GEOCODE_KEY

def GetLocationCoordinates(city):
    url = f'https://geocode.xyz/{city}?json=1&auth={GEOCODE_KEY}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            geoloc = response.json()
            response.close()
            return geoloc
        else:
            print("Failed to fetch location information:", response.status_code)
            return []
    except Exception as e:
        print("Error fetching location information:", e)
        return []

