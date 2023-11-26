import json
import logging
import azure.functions as func
from sensor import Sensor, SensorStat
from db import DB_Connection


def get_initial_sensor_data(sensor: Sensor) -> SensorStat:
    return SensorStat(
        sensor_id=sensor.sensor_id,
        min_temperature=sensor.temperature,
        max_temperature=sensor.temperature,
        avg_temperature=sensor.temperature,
        min_relative_humidity=sensor.relative_humidity,
        max_relative_humidity=sensor.relative_humidity,
        avg_relative_humidity=sensor.relative_humidity,
        min_co2=sensor.co2,
        max_co2=sensor.co2,
        avg_co2=sensor.co2,
        min_wind_speed=sensor.wind_speed,
        max_wind_speed=sensor.wind_speed,
        avg_wind_speed=sensor.wind_speed,
        count=1,
    )


def get_new_sensor_stat(sensor: Sensor, sensor_stat: SensorStat) -> SensorStat:
    sensor_stat.max_co2 = max(sensor.co2, sensor_stat.max_co2)
    sensor_stat.max_relative_humidity = max(
        sensor.relative_humidity, sensor_stat.max_relative_humidity
    )
    sensor_stat.max_temperature = max(sensor.temperature, sensor_stat.max_temperature)
    sensor_stat.max_wind_speed = max(sensor.wind_speed, sensor_stat.max_wind_speed)

    sensor_stat.min_co2 = min(sensor.co2, sensor_stat.min_co2)
    sensor_stat.min_relative_humidity = min(
        sensor.relative_humidity, sensor_stat.min_relative_humidity
    )
    sensor_stat.min_temperature = min(sensor.temperature, sensor_stat.min_temperature)
    sensor_stat.min_wind_speed = min(sensor.wind_speed, sensor_stat.min_wind_speed)

    sensor_stat.avg_co2 = (sensor.co2 + (sensor_stat.avg_co2 * sensor_stat.count)) / (
        sensor_stat.count + 1
    )
    sensor_stat.avg_relative_humidity = (
        sensor.relative_humidity
        + (sensor_stat.avg_relative_humidity * sensor_stat.count)
    ) / (sensor_stat.count + 1)
    sensor_stat.avg_temperature = (
        sensor.temperature + (sensor_stat.avg_temperature * sensor_stat.count)
    ) / (sensor_stat.count + 1)
    sensor_stat.avg_wind_speed = (
        sensor.wind_speed + (sensor_stat.avg_wind_speed * sensor_stat.count)
    ) / (sensor_stat.count + 1)
    sensor_stat.count += 1
    return sensor_stat


def main(data: str):
    logging.info("SQL Trigger activated")

    logging.info("Parsing sensor data")
    sensor_map: dict[int, Sensor] = {}
    for obj in json.loads(data):
        sensor = Sensor(**obj["Item"])
        sensor_map[sensor.sensor_id] = sensor

    logging.info("Creating new connection to database")
    db = DB_Connection()

    logging.info("Getting all current current sensor statistics")
    cursor = db.execute(
        """
        SELECT * FROM SensorStat;
        """
    )
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()

    if len(rows) == 0:
        logging.info(
            "Empty sensor stat table, inserting current sensor into sensor stat table"
        )
        sensor_stat_list_to_insert = [
            get_initial_sensor_data(sensor_map[x]) for x in sensor_map.keys()
        ]
        for sensor_stat_insert in sensor_stat_list_to_insert:
            print(sensor_stat_insert)
            db.add_to_sensor_stat(sensor_stat=sensor_stat_insert)
        db.commit()
        db.stop()
        return

    logging.info("Parsing sensor stats into a map")
    sensor_stat_map: dict[int, SensorStat] = {}
    for row in rows:
        sensor_stat = SensorStat(**dict(zip(columns, row)))
        sensor_stat_map[sensor_stat.sensor_id] = sensor_stat

    logging.info("Adding sensor statistics data into table")
    for i in range(20):
        check_sensor_id = i + 1
        sensor = sensor_map[check_sensor_id]
        sensor_stat = sensor_stat_map[check_sensor_id]
        sensor_stat = get_new_sensor_stat(sensor=sensor, sensor_stat=sensor_stat)
        db.alter_sensor_stat(sensor_stat=sensor_stat)

    logging.info("Committing to database")
    db.commit()

    logging.info("Stopping connection to database")
    db.stop()
