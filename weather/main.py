#!/usr/bin/env python3
"""
Консольное приложение для получения текущей погоды
Использует API open-meteo.com с кэшированием результатов
"""

from parser import create_parser
from commands import get_weather_command

def main():
    """Основная функция приложения"""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        result = get_weather_command(args)
        print(result)
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    main()