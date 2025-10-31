from . import api, cache

def handle_command(args):
    if args.command == "city":
        city = args.name
        cached = cache.get_from_cache(city)
        if cached:
            print(f"[КЭШ] Погода в {city}: {cached['temperature']}°C, ветер {cached['windspeed']} м/с")
            return

        print("Получаю данные с API...")
        lat, lon = api.get_coords_by_city(city)
        weather = api.get_weather_by_coords(lat, lon)
        cache.save_to_cache(city, weather)
        print(f"Погода в {city}: {weather['temperature']}°C, ветер {weather['windspeed']} м/с")

    elif args.command == "coords":
        key = f"{args.lat},{args.lon}"
        cached = cache.get_from_cache(key)
        if cached:
            print(f"[КЭШ] Погода ({key}): {cached['temperature']}°C, ветер {cached['windspeed']} м/с")
            return

        print("Получаю данные с API...")
        weather = api.get_weather_by_coords(args.lat, args.lon)
        cache.save_to_cache(key, weather)
        print(f"Погода ({key}): {weather['temperature']}°C, ветер {weather['windspeed']} м/с")