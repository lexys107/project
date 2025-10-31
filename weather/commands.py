from .api import WeatherAPI
from .cache import WeatherCache
from .parser import create_parser

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
        61: 'Небольшой дождь',
        63: 'Умеренный дождь',
        65: 'Сильный дождь',
        80: 'Ливень',
        95: 'Гроза'
    }
    
    weather_desc = weather_descriptions.get(weather_code, 'Неизвестно')
    wind_dir = get_wind_direction(wind_direction)
    
    result = [
        "┌──────────────────────────────┐",
        "│           ПОГОДА             │",
        "├──────────────────────────────┤",
        f"│ Температура: {temp_value:5.1f} {temp_unit:3} │",
        f"│ Погода: {weather_desc:19} │",
        f"│ Ветер: {wind_speed:3.1f} м/с, {wind_dir:2}     │",
        f"│ Время: {time:19} │",
        "└──────────────────────────────┘"
    ]
    
    return '\n'.join(result)

def execute_command():
    """Выполнить команду на основе аргументов"""
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