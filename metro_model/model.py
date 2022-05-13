import asyncio
import base64
import io
import pprint
import time
import random
import matplotlib.pyplot as plt

from fastapi_socketio import SocketManager

from models import *
from storage import *


class Metro:
    def __init__(self, trains, speed, sm: SocketManager):
        self.trains_count = trains
        self.speed = speed
        self.loop = asyncio.get_event_loop()
        self.stations = []
        self.trains = []
        self.START_TIME = 0
        self.average_people_in_station = []
        self.average_people_in_wagon = []
        self.average_time_travel = []
        self.times = []
        self.emitter = sm.emit

    async def init(self):
        self.START_TIME = time.time()
        # Create stations
        for i in stations_names:
            station = Station(i)
            self.loop.create_task(station.passengers_in(self.speed, self.emitter))
            self.stations.append(station)

        # Create trains
        self.loop.create_task(self.create_trains(self.trains_count // 2))

        # Start graphs
        self.loop.create_task(self.graphs())

        # self.loop.create_task(self.stations_getter())
        # self.loop.create_task(self.get_trains())
        self.loop.create_task(self.send_data())
        self.loop.create_task(self.send_graph())

    async def create_trains(self, count):
        for i in range(count):
            train_1 = RollingStock(self.stations[0].name)
            train_2 = RollingStock(self.stations[4].name)
            train_2.pixel_x = 1390
            self.trains.append(train_1)
            self.trains.append(train_2)
            self.loop.create_task(train_1.get_on_passengers(self.stations))
            self.loop.create_task(train_2.get_on_passengers(self.stations))
            await asyncio.sleep(((38 * 60 * ONE_SECOND) / (count * 2)))

    async def graphs(self):
        while True:
            current_time = time.time()
            self.times.append(current_time - self.START_TIME)
            passengers = get_passengers()
            try:
                self.average_people_in_station.append(
                    sum(
                        [
                            (
                                station.capacity["left"].qsize()
                                if "left" in station.capacity
                                else 0
                            )
                            + (
                                station.capacity["rigth"].qsize()
                                if "rigth" in station.capacity
                                else 0
                            )
                            for station in self.stations
                        ]
                    )
                    / len(self.stations)
                )
            except ZeroDivisionError:
                self.average_people_in_station.append(0)

            try:
                self.average_people_in_wagon.append(
                    sum([train.current_capacity.qsize() for train in self.trains])
                    / len(self.trains)
                )
            except ZeroDivisionError:
                self.average_people_in_wagon.append(0)

            avg_time = []
            for people in passengers:
                if people.is_finish:
                    avg_time.append(people.time)
            try:
                self.average_time_travel.append(sum(avg_time) / len(avg_time))
            except ZeroDivisionError:
                self.average_time_travel.append(0)

            await asyncio.sleep(1 * ONE_SECOND)

    def stop(self):
        self.loop.stop()

    async def stations_getter(self):
        res = {v.name: (
                               v.capacity["left"].qsize()
                               if "left" in v.capacity
                               else 0
                           )
                           + (
                               v.capacity["right"].qsize()
                               if "right" in v.capacity
                               else 0
                           ) for v in self.stations}

        await asyncio.sleep(0.0)
        return res

    async def get_trains(self):
        res = []
        curr_time = time.time()
        for train in self.trains:
            data = {"current_capacity": train.current_capacity.qsize()}
            delta = (curr_time - train.start_time) / ONE_SECOND
            cutted = delta % 2310
            pixels = cutted * (2800 / 2310)
            train.pixel_x = train.pixel_x + train.sign
            if train.pixel_x > 1400 or train.pixel_x < 1:
                train.sign = -train.sign
            # if pixels > 1399 or pixels < 1:
            #     # pixel = 1300
            #     # 1400 - 1300 = 100
            #     delta =- delta
            #     data["y"] = 0
            #     # data["x"] = pixels
            # else:
            #     pixels = pixels
            #     data["y"] = 0
            data["x"] = train.pixel_x
            # if abs(train.pixel_x) > 1400:
            #     raise ValueError(train.pixel_x)
            res.append(data)
        # print()
        # pprint.pp(res)
        await asyncio.sleep(0.0)
        return res

    def graph_build(self):
        plt.clf()
        plt.fill()
        length = len(self.times)
        plt.plot(
            self.times,
            self.average_people_in_station[0:length],
            c="blue",
            label="Среднее количество пассажиров в станции",
        )
        plt.plot(
            self.times,
            self.average_people_in_wagon[0:length],
            c="red",
            label="Среднее количество пассажиров в поезде",
        )
        plt.plot(self.times, self.average_time_travel[0:length], c="green", label="Среднее время пути")
        plt.legend()
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png', transparent=True)
        img = base64.encodebytes(img_buf.getvalue()).decode()

        return img

    async def send_data(self):
        while True:
            train_send = await self.get_trains()
            station_send = await self.stations_getter()
            await self.emitter("trains", train_send)
            await self.emitter("stations", station_send)

            await asyncio.sleep(0.1)

    async def send_graph(self):
        while True:
            image = self.graph_build()

            await self.emitter("image", image)
            await asyncio.sleep(2)



