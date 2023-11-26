from pydantic import BaseModel
import random
import uuid


class Sensor(BaseModel):
    group_id: str
    sensor_id: int
    temperature: int
    wind_speed: int
    relative_humidity: int
    co2: int


class SensorStat(BaseModel):
    sensor_id: int
    max_temperature: int
    min_temperature: int
    avg_temperature: float
    max_wind_speed: int
    min_wind_speed: int
    avg_wind_speed: float
    max_relative_humidity: int
    min_relative_humidity: int
    avg_relative_humidity: float
    max_co2: int
    min_co2: int
    avg_co2: float
    count: int


NUMBER_OF_SENSORS = 20


def random_number(start: int, end: int):
    return random.randint(start, end)


def generate_random_data(num_of_sensors: int = NUMBER_OF_SENSORS) -> list[Sensor]:
    sensor_list = []
    group_id = str(uuid.uuid1())
    for i in range(num_of_sensors):
        sensor_list.append(
            Sensor(
                group_id=group_id,
                sensor_id=i + 1,
                temperature=random_number(8, 15),
                wind_speed=random_number(15, 25),
                relative_humidity=random_number(40, 70),
                co2=random_number(500, 1500),
            )
        )

    return sensor_list
