CREATE TABLE SensorStat (
    [sensor_id] INT NOT NULL, -- uuid
    [max_temperature] INT NOT NULL,
    [min_temperature] INT NOT NULL,
    [avg_temperature] FLOAT NOT NULL,
    [max_wind_speed] INT NOT NULL,
    [min_wind_speed] INT NOT NULL,
    [avg_wind_speed] FLOAT NOT NULL,
    [max_relative_humidity] INT NOT NULL,
    [min_relative_humidity] INT NOT NULL,
    [avg_relative_humidity] FLOAT NOT NULL,
    [max_co2] INT NOT NULL,
    [min_co2] INT NOT NULL,
    [avg_co2] FLOAT NOT NULL,
    [count] INT NOT NULL,
    PRIMARY KEY (sensor_id)
);