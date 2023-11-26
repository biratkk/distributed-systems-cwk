CREATE TABLE Sensor (
    [group_id] NVARCHAR(36),
    [sensor_id] INT NOT NULL, -- uuid
    [temperature] INT NOT NULL,
    [wind_speed] INT NOT NULL,
    [relative_humidity] INT NOT NULL,
    [co2] INT NOT NULL,
    PRIMARY KEY (group_id, sensor_id)
);

ALTER DATABASE [distributed-cwk-db]
SET CHANGE_TRACKING = ON
(CHANGE_RETENTION = 2 DAYS, AUTO_CLEANUP = ON);

ALTER TABLE [Sensor]
ENABLE CHANGE_TRACKING;