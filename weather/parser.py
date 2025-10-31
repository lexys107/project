import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="Показ погоды по названию города или координатам.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Получение погоды по городу
    city_parser = subparsers.add_parser("city", help="Показ погоды по названию города")
    city_parser.add_argument("name", help="Название города")

    # Получение погоды по координатам
    coords_parser = subparsers.add_parser("coords", help="Показ погоды по координатам")
    coords_parser.add_argument("lat", type=float, help="Широта")
    coords_parser.add_argument("lon", type=float, help="Долгота")

    return parser