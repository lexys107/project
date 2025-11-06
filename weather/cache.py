import json
import os
import time
from datetime import datetime, timedelta

class WeatherCache:
    def __init__(self, cache_file='weather_cache.json', ttl_hours=1):
        self.cache_file = cache_file
        self.ttl = timedelta(hours=ttl_hours)
        self._ensure_cache_file()
    
    def _ensure_cache_file(self):
        """Создает файл кэша, если он не существует"""
        if not os.path.exists(self.cache_file):
            with open(self.cache_file, 'w') as f:
                json.dump({}, f)
    
    def get(self, key):
        """Получает данные из кэша по ключу"""
        try:
            if not os.path.exists(self.cache_file):
                return None
                
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            if key in cache:
                cached_data = cache[key]
                # Проверяем, не истекло ли время жизни кэша
                cached_time = datetime.fromisoformat(cached_data['timestamp'])
                if datetime.now() - cached_time < self.ttl:
                    return cached_data['data']
                else:
                    # Удаляем просроченные данные
                    self._remove_expired()
                    return None
                    
        except (json.JSONDecodeError, KeyError, ValueError, IOError) as e:
            print(f"Ошибка чтения кэша: {e}")
            return None
    
    def set(self, key, data):
        """Сохраняет данные в кэш"""
        try:
            # Читаем существующий кэш
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache = json.load(f)
            else:
                cache = {}
            
            # Обновляем кэш
            cache[key] = {
                'timestamp': datetime.now().isoformat(),
                'data': data
            }
            
            # Записываем обратно
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Ошибка кэширования: {e}")
    
    def _remove_expired(self):
        """Удаляет все просроченные записи"""
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
            
            # Фильтруем просроченные записи
            current_time = datetime.now()
            valid_cache = {}
            
            for key, value in cache.items():
                cached_time = datetime.fromisoformat(value['timestamp'])
                if current_time - cached_time < self.ttl:
                    valid_cache[key] = value
            
            # Сохраняем обратно
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(valid_cache, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Ошибка очистки кэша: {e}")