import datetime
import logging
from sensor import generate_random_data
from db import DB_Connection
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    logging.info("Triggered timer trigger")

    if mytimer.past_due:
        logging.info("The timer is past due!")

    logging.info("Generating random data")
    data = generate_random_data()

    logging.info("Adding data to azure db")
    db = DB_Connection()
    for sensor in data:
        db.add_to_sensor(sensor)

    db.commit()

    logging.info("Closing connection to azure db")
    db.stop()
