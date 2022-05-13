import asyncio
import random
import time
from .consts import *


class RollingStock:
    # Class variables
    CAPACITY = 200

    def __init__(self, start_station) -> None:
        self.current_capacity = asyncio.Queue(self.CAPACITY)
        self.current_station = start_station
        self.start_time = time.time()
        self.pixel_x = 0
        self.sign = random.randint(2, 10)

        if start_station == "Рокоссовская":
            self.direction = "right"
            self.step = 1
            self.index = 0
            self.x = 0
        elif start_station == "Библиотека им. Глеба":
            self.direction = "left"
            self.step = -1
            self.index = 4
            self.x = 1400

    def get_out_passengers(self):
        if self.current_capacity.qsize() != 0:
            temp = asyncio.Queue(self.CAPACITY)
            for _ in range(self.current_capacity.qsize()):
                people = self.current_capacity.get_nowait()
                if people.destination != self.current_station:
                    temp.put_nowait(people)
                    continue
                people.finish()
            self.current_capacity = temp

    def get_on_the_train(self, stations):
        queue = stations[self.index].capacity[self.direction]

        while True:
            arrive_time = time.time()

            people = None
            if (time.time() - arrive_time) >= (DELAY * ONE_SECOND):
                print("limit")
                break
            try:
                people = queue.get_nowait()
                self.current_capacity.put_nowait(people)
            except asyncio.QueueEmpty:
                break
            except asyncio.QueueFull:
                if people:
                    queue.put_nowait(people)
                break

    async def get_on_passengers(self, stations):
        while True:

            # print(
            #     f"Train arrived at {stations[self.index].name} at {arrive_time - START_TIME}"
            # )
            self.get_out_passengers()
            # print(f"{time.time() - arrive_time} Start taking passengers")

            self.get_on_the_train(stations)


            # print(f"{time.time() - arrive_time} Stop taking passangers")
            await asyncio.sleep(DELAY * ONE_SECOND)
            # print(
            #     f"{time.time() - arrive_time} {self.current_capacity.qsize()} people in train"
            # )
            # next station
            self.index += self.step
            if self.index == len(stations) - 1 and self.direction == "right":
                self.step = -1
                self.direction = "left"
                self.get_on_the_train(stations)
            elif self.index == 0 and self.direction == "left":
                self.step = 1
                self.direction = "right"
                self.get_on_the_train(stations)
            # print(f"Train is going to {stations[self.index].name}")
            # print(time_to_station[(self.current_station, stations[self.index].name)])
            await asyncio.sleep(
                time_to_station[(self.current_station, stations[self.index].name)]
            )
            self.current_station = stations[self.index].name
