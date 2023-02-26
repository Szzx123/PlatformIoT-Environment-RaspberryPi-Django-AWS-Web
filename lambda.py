import json
import psycopg2
from datetime import datetime


def lambda_handler(event, context):
    print(event)
    print(context)

    # Connect to the AWS PostgreSQL database
    conn = psycopg2.connect(
        host='HOST',
        port='PORT',
        database='DATABASE',
        user='USER',
        password='PASSWORD'
    )

    # Create a cursor
    cur = conn.cursor()

    sample_time = datetime.now()

    cur.execute("INSERT INTO appenv_temperature (temperature, sample_time, device_id) VALUES (%s, %s, %s)",
                (event['temperature'], sample_time, event['device_id']))
    cur.execute("INSERT INTO appenv_humidity (humidity, sample_time, device_id) VALUES (%s, %s, %s)",
                (event['humidity'], sample_time, event['device_id']))
    cur.close()

    conn.commit()
    conn.close()
