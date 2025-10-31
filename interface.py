import tkinter as tk
from tkinter import messagebox
from weather import api, cache

def show_weather():
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Ошибка", "Введите название города!")
        return

    cached = cache.get_from_cache(city)
    if cached:
        weather = cached
        source = " (из кэша)"
    else:
        try:
            lat, lon = api.get_coords_by_city(city)
            weather = api.get_weather_by_coords(lat, lon)
            cache.save_to_cache(city, weather)
            source = " (с API)"
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось получить погоду: {e}")
            return

    result_label.config(
        text=f"Погода в {city}{source}:\nТемпература: {weather['temperature']}°C\nВетер: {weather['windspeed']} м/с"
    )

# --- Интерфейс ---
root = tk.Tk()
root.title("Погода (Weather CLI GUI)")
root.geometry("350x250")

tk.Label(root, text="Введите город:", font=("Arial", 12)).pack(pady=10)
city_entry = tk.Entry(root, width=25)
city_entry.pack()

tk.Button(root, text="Показать погоду", command=show_weather).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 11), justify="center")
result_label.pack(pady=10)

root.mainloop()