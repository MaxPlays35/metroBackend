from models import People

passengers = []
finished = []


def add_passengers(passenger: People):
    passengers.append(passenger)


def get_passengers():
    return passengers

