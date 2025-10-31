import json
import os
from datetime import datetime, timedelta

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