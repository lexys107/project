#!/usr/bin/env python3
"""
Консольное приложение для показа погоды
Использует API open-meteo.com с кэшированием
"""

import argparse
import requests
import json
import os
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
            'волгоград': (48.7080, 44.5133),
            'сочи': (43.5855, 39.7231),
            'краснодар': (45.0355, 38.9750),
            'саратов': (51.5336, 46.0343),
            'тюмень': (57.1530, 65.5343),
            'иркутск': (52.2864, 104.2806)
        }
        
        city_lower = city_name.lower()
        if city_lower in city_coords:
            latitude, longitude = city_coords[city_lower]
            return self.get_weather_by_coords(latitude, longitude)
        else:
            raise Exception(f"Город '{city_name}' не найден в базе. Используйте координаты.")


class WeatherCache:
    def __init__(self, cache_file: str = "weather_cache.json"):
        self.cache_file = cache_file
        self.cache_duration = timedelta(hours=1)  # Кэшируем на 1 час
    
    def _load_cache(self) -> dict:
        """Загрузить кэш из файла"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_cache(self, cache: dict):
        """Сохранить кэш в файл"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, ensure_ascii=False, indent=2)
        except IOError as e:
            print(f"Ошибка сохранения кэша: {e}")
    
    def get(self, key: str) -> dict | None:
        """Получить данные из кэша"""
        cache = self._load_cache()
        
        if key in cache:
            cached_data = cache[key]
            cache_time = datetime.fromisoformat(cached_data['timestamp'])
            
            if datetime.now() - cache_time < self.cache_duration:
                return cached_data['data']
            else:
                # Удалить просроченные данные
                del cache[key]
                self._save_cache(cache)
        
        return None
    
    def set(self, key: str, data: dict):
        """Сохранить данные в кэш"""
        cache = self._load_cache()
        
        cache[key] = {
            'timestamp': datetime.now().isoformat(),
            'data': data
        }
        
        self._save_cache(cache)
    
    def generate_key(self, latitude: float = None, longitude: float = None, city: str = None) -> str:
        """Сгенерировать ключ для кэша"""
        if city:
            return f"city_{city.lower()}"
        elif latitude is not None and longitude is not None:
            return f"coords_{round(latitude, 2)}_{round(longitude, 2)}"
        else:
            raise ValueError("Должны быть указаны либо город, либо координаты")


def create_parser():
    """Создать парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Консольное приложение для показа погоды',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python main.py --city Москва
  python main.py --coords 55.7558 37.6173
  python main.py --city Санкт-Петербург --units fahrenheit
  python main.py --city Новосибирск --no-cache
        '''
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--city',
        type=str,
        help='Название города (например: Москва)'
    )
    group.add_argument(
        '--coords',
        type=float,
        nargs=2,
        metavar=('LATITUDE', 'LONGITUDE'),
        help='Координаты (например: 55.7558 37.6173)'
    )
    
    parser.add_argument(
        '--units',
        type=str,
        choices=['celsius', 'fahrenheit'],
        default='celsius',
        help='Единицы измерения температуры (по умолчанию: celsius)'
    )
    
    parser.add_argument(
        '--no-cache',
        action='store_true',
        help='Не использовать кэш'
    )
    
    return parser


def temperature_to_units(temperature: float, units: str) -> float:
    """Конвертировать температуру в нужные единицы"""
    if units == 'fahrenheit':
        return (temperature * 9/5) + 32
    return temperature


def get_wind_direction(degree: float) -> str:
    """Определить направление ветра по градусам"""
    directions = ['С', 'СВ', 'В', 'ЮВ', 'Ю', 'ЮЗ', 'З', 'СЗ']
    index = round(degree / 45) % 8
    return directions[index]


def format_weather_data(weather_data: dict, units: str = 'celsius') -> str:
    """Отформатировать данные о погоде для вывода"""
    current = weather_data.get('current_weather', {})
    
    temperature = current.get('temperature', 0)
    wind_speed = current.get('windspeed', 0)
    wind_direction = current.get('winddirection', 0)
    weather_code = current.get('weathercode', 0)
    time = current.get('time', '')
    
    # Конвертируем температуру
    temp_value = temperature_to_units(temperature, units)
    temp_unit = '°C' if units == 'celsius' else '°F'
    
    # Описание погоды по коду
    weather_descriptions = {
        0: 'Ясно',
        1: 'Преимущественно ясно',
        2: 'Переменная облачность',
        3: 'Пасмурно',
        45: 'Туман',
        48: 'Туман с инеем',
        51: 'Лежащая морось',
        53: 'Морось',
        55: 'Сильная морось',
        56: 'Ледяная морось',
        57: 'Сильная ледяная морось',
        61: 'Небольшой дождь',
        63: 'Умеренный дождь',
        65: 'Сильный дождь',
        66: 'Ледяной дождь',
        67: 'Сильный ледяной дождь',
        71: 'Небольшой снег',
        73: 'Умеренный снег',
        75: 'Сильный снег',
        77: 'Снежные зерна',
        80: 'Небольшой ливень',
        81: 'Умеренный ливень',
        82: 'Сильный ливень',
        85: 'Небольшой снегопад',
        86: 'Сильный снегопад',
        95: 'Гроза',
        96: 'Гроза с градом',
        99: 'Сильная гроза с градом'
    }
    
    weather_desc = weather_descriptions.get(weather_code, 'Неизвестно')
    wind_dir = get_wind_direction(wind_direction)
    
    # Форматируем время
    if time:
        try:
            dt = datetime.fromisoformat(time.replace('Z', '+00:00'))
            formatted_time = dt.strftime("%d.%m.%Y %H:%M")
        except:
            formatted_time = time
    else:
        formatted_time = "Неизвестно"
    
    result = [
        "┌──────────────────────────────┐",
        "│           ПОГОДА             │",
        "├──────────────────────────────┤",
        f"│ Температура: {temp_value:5.1f} {temp_unit:3} │",
        f"│ Погода: {weather_desc:19} │",
        f"│ Ветер: {wind_speed:3.1f} м/с, {wind_dir:2}     │",
        f"│ Время: {formatted_time:19} │",
        "└──────────────────────────────┘"
    ]
    
    return '\n'.join(result)


def main():
    """Основная функция приложения"""
    parser = create_parser()
    args = parser.parse_args()
    
    api = WeatherAPI()
    cache = WeatherCache()
    
    try:
        # Генерируем ключ для кэша
        if args.city:
            cache_key = cache.generate_key(city=args.city)
            # Проверяем кэш, если не отключен
            if not args.no_cache:
                cached_data = cache.get(cache_key)
                if cached_data:
                    print("📁 Данные из кэша:")
                    print(format_weather_data(cached_data, args.units))
                    return
            
            # Получаем данные из API
            weather_data = api.get_weather_by_city(args.city)
            # Сохраняем в кэш
            if not args.no_cache:
                cache.set(cache_key, weather_data)
            
        else:  # coordinates
            lat, lon = args.coords
            cache_key = cache.generate_key(latitude=lat, longitude=lon)
            
            # Проверяем кэш, если не отключен
            if not args.no_cache:
                cached_data = cache.get(cache_key)
                if cached_data:
                    print("📁 Данные из кэша:")
                    print(format_weather_data(cached_data, args.units))
                    return
            
            # Получаем данные из API
            weather_data = api.get_weather_by_coords(lat, lon)
            # Сохраняем в кэш
            if not args.no_cache:
                cache.set(cache_key, weather_data)
        
        print("🌤️  Данные из API:")
        print(format_weather_data(weather_data, args.units))
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    main()