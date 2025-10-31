import argparse

def create_parser():
    """Создать парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Консольное приложение для показа погоды',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python main.py --city Москва
  python main.py --coords 55.7558 37.6173
  python main.py --city Санкт-Петербург --units celsius
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