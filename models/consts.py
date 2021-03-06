DELAY = 15
SPEED = 50
STATION_CAPACITY = 1000
DELAY_BETWEEN_TRAINS = 45
ONE_SECOND = 0.01

stations_names = [
    "Рокоссовская",
    "Соборная",
    "Кристалл",
    "Заречная",
    "Библиотека им. Глеба",
]

time_to_station = {
    ("Рокоссовская", "Соборная"): (6 * 60) * ONE_SECOND,
    ("Соборная", "Кристалл"): (3 * 60) * ONE_SECOND,
    ("Кристалл", "Заречная"): (2 * 60) * ONE_SECOND,
    ("Заречная", "Библиотека им. Глеба"): (7 * 60) * ONE_SECOND,
    ("Библиотека им. Глеба", "Заречная"): (7 * 60) * ONE_SECOND,
    ("Заречная", "Кристалл"): (2 * 60) * ONE_SECOND,
    ("Кристалл", "Соборная"): (3 * 60) * ONE_SECOND,
    ("Соборная", "Рокоссовская"): (6 * 60) * ONE_SECOND,
}
