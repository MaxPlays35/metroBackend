import asyncio

from fastapi_socketio import SocketManager

from .consts import *
from .People import People
from storage import add_passengers


class Station:
    def __init__(self, name) -> None:
        self.name = name
        if name == "Рокоссовская":
            self.capacity = {"right": asyncio.Queue()}
        elif name == "Библиотека им. Глеба":
            self.capacity = {"left": asyncio.Queue()}
        else:
            self.capacity = {"left": asyncio.Queue(), "right": asyncio.Queue()}

    async def passengers_in(self, count, emitter: SocketManager.emit):
        while True:
            people = People(self.name)
            add_passengers(people)
            count_of_people = (
                self.capacity["left"].qsize() if "left" in self.capacity else 0
            ) + (self.capacity["right"].qsize() if "right" in self.capacity else 0)
            if count_of_people + 1 > STATION_CAPACITY:
                await emitter("overflow_station", self.name)
                print(f"Overflow in {self.name} {count_of_people}")
                exit(1)
            if people.direction == "left":
                await self.capacity["left"].put(people)
            else:
                await self.capacity["right"].put(people)

            count_of_people = (
                                  self.capacity["left"].qsize() if "left" in self.capacity else 0
                              ) + (self.capacity["right"].qsize() if "right" in self.capacity else 0)
            # await emitter("passengers_in", {"station": self.name, "count": count_of_people})
            # print(f"{self.name} {count} people in {len(debug)}")
            # print("Finish add people")

            # print(
            #     f"{self.name} - {(self.capacity['left'].qsize() if 'left' in self.capacity else 0) + (self.capacity['rigth'].qsize() if 'rigth' in self.capacity else 0)}"
            # )
            await asyncio.sleep(1 * ONE_SECOND)
