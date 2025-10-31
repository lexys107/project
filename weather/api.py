import requests
import json
from datetime import datetime, timedelta

class WeatherAPI:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
    
    def get_weather_by_coords(self, latitude: float, longitude: float) -> dict:
        """Получить погоду по координатам"""
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': True,
            'timezone': 'auto',
            'forecast_days': 1
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка API: {e}")
    
    def get_weather_by_city(self, city_name: str) -> dict:
        """Получить погоду по названию города (через геокодинг)"""
        # Простой геокодинг для популярных городов
        city_coords = {
            'москва': (55.7558, 37.6173),
            'санкт-петербург': (59.9343, 30.3351),
            'новосибирск': (55.0084, 82.9357),
            'екатеринбург': (56.8389, 60.6057),
            'казань': (55.7961, 49.1064),
            'нижний новгород': (56.3269, 44.0075),
            'челябинск': (55.1644, 61.4368),
            'самара': (53.1951, 50.1069),
            'омск': (54.9924, 73.3686),
            'ростов-на-дону': (47.2225, 39.7187),
            'уфа': (54.7355, 55.9587),
            'красноярск': (56.0153, 92.8932),
            'пермь': (58.0105, 56.2502),
            'воронеж': (51.6720, 39.1843),
            'волгоград': (48.7080, 44.5133)
        }
        
        city_lower = city_name.lower()
        if city_lower in city_coords:
            latitude, longitude = city_coords[city_lower]
            return self.get_weather_by_coords(latitude, longitude)
        else:
            raise Exception(f"Город '{city_name}' не найден в базе. Используйте координаты.")