import random
import copy
import string
import time
from .consts import *


class People:
    def __init__(self, start_station) -> None:
        self.name = "".join(random.choice(string.ascii_letters) for _ in range(10))
        t = copy.copy(stations_names)
        t.remove(start_station)
        self.destination = random.choice(t)
        self.direction = (
            "rigth"
            if stations_names.index(start_station)
            < stations_names.index(self.destination)
            else "left"
        )
        self.start_time = time.time()
        self.is_finish = False

    def finish(self):
        self.is_finish = True
        self.finish_time = time.time()
        self.time = self.finish_time - self.start_time
