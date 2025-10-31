import requests

def get_weather_by_coords(lat, lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    return data["current_weather"]

def get_coords_by_city(city):
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
    if "results" not in data:
        raise ValueError("Город не найден.")
    coords = data["results"][0]
    return coords["latitude"], coords["longitude"]