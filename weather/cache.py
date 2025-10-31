import json
import os
from datetime import datetime, timedelta

CACHE_FILE = "weather_cache.json"
CACHE_TTL = timedelta(minutes=10)

def _load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def _save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_from_cache(key):
    cache = _load_cache()
    if key in cache:
        record = cache[key]
        timestamp = datetime.fromisoformat(record["time"])
        if datetime.now() - timestamp < CACHE_TTL:
            return record["data"]
    return None

def save_to_cache(key, data):
    cache = _load_cache()
    cache[key] = {"data": data, "time": datetime.now().isoformat()}
    _save_cache(cache)