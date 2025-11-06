import argparse

def create_parser():
    """Создает парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description='Получение текущей погоды',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python main.py --city "Москва"
  python main.py --coords 55.7558 37.6173
  python main.py -c "Лондон"
        '''
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--city', '-c',
        type=str,
        help='Название города (например: "Москва")'
    )
    group.add_argument(
        '--coords', 
        nargs=2,
        type=float,
        metavar=('LATITUDE', 'LONGITUDE'),
        help='Координаты (например: 55.7558 37.6173)'
    )
    
    return parser