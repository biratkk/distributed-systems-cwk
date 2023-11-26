from dotenv import load_dotenv
import os
import pyodbc
from pyodbc import Connection, Cursor
from sensor import Sensor, SensorStat

load_dotenv()


class DB_Connection:
    CONNECTION_STRING = os.environ.get("CONNECTION_STRING")
    cursor: Cursor | None = None
    connection: Connection | None = None

    def __init__(self):
        try:
            self.connection = pyodbc.connect(self.CONNECTION_STRING)
        except:
            raise AttributeError(
                "Unable to connect to the database server, please make sure the server is online!"
            )

    def add_to_sensor(self, sensor: Sensor):
        self.execute(
            f"""
    INSERT INTO Sensor (group_id,sensor_id,wind_speed,temperature,relative_humidity,co2) VALUES ('{sensor.group_id}',{sensor.sensor_id},{sensor.wind_speed},{sensor.temperature},{sensor.relative_humidity},{sensor.co2})
            """
        )

    def add_to_sensor_stat(self, sensor_stat: SensorStat):
        self.execute(
            f"""
            INSERT INTO SensorStat (sensor_id,
            min_wind_speed,
            max_wind_speed,
            avg_wind_speed,
            min_temperature,
            max_temperature,
            avg_temperature,
            min_relative_humidity,
            max_relative_humidity,
            avg_relative_humidity,
            min_co2,
            max_co2,
            avg_co2,
            count)
            VALUES 
            ({sensor_stat.sensor_id},
            {sensor_stat.min_wind_speed},
            {sensor_stat.max_wind_speed},
            {sensor_stat.avg_wind_speed},
            {sensor_stat.min_temperature},
            {sensor_stat.max_temperature},
            {sensor_stat.avg_temperature},
            {sensor_stat.min_relative_humidity},
            {sensor_stat.max_relative_humidity},
            {sensor_stat.avg_relative_humidity},
            {sensor_stat.min_co2},
            {sensor_stat.max_co2},
            {sensor_stat.avg_co2},
            {sensor_stat.count})
            """
        )

    def alter_sensor_stat(self, sensor_stat: SensorStat):
        self.execute(
            f"""
            UPDATE SensorStat 
            SET sensor_id = {sensor_stat.sensor_id},
            min_wind_speed = {sensor_stat.min_wind_speed},
            max_wind_speed = {sensor_stat.max_wind_speed},
            avg_wind_speed = {sensor_stat.avg_wind_speed},
            min_temperature = {sensor_stat.min_temperature},
            max_temperature = {sensor_stat.max_temperature},
            avg_temperature = {sensor_stat.avg_temperature},
            min_relative_humidity = {sensor_stat.min_relative_humidity},
            max_relative_humidity = {sensor_stat.max_relative_humidity},
            avg_relative_humidity = {sensor_stat.avg_relative_humidity},
            min_co2 = {sensor_stat.min_co2},
            max_co2 = {sensor_stat.max_co2},
            avg_co2 = {sensor_stat.avg_co2},
            count = {sensor_stat.count}
            WHERE sensor_id = {sensor_stat.sensor_id}
            """
        )

    def execute(self, query: str):
        if self.cursor is None:
            self.cursor = self.connection.cursor()
        return self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    def stop(self):
        self.cursor.close()
        self.connection.close()
