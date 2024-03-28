import time

from paho.mqtt import client as mqtt_client

from generate_height_data import generate_height_data
from src.file_datasource import FileDatasource
from src.schema.aggregated_data_schema import AggregatedDataSchema

from config import (
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_TOPIC,
    DELAY,
)


def connect_mqtt(broker, port):
    # Create MQTT client
    print(f"Connecting to {broker}:{port}")

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print(f"Failed to connect {broker}:{port}, return code {rc}")
            exit(rc)  # Stop execution

    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()

    return client


def publish(client, topic, datasource, delay):
    datasource.start_reading()

    while True:
        time.sleep(delay)
        data = datasource.read()
        msg = AggregatedDataSchema().dumps(data)
        result = client.publish(topic, msg)

        status = result[0]

        if status == 0:
            pass

        else:
            print(f"Failed to send message to topic {topic}")


def run():
    # Prepare mqtt-agent client
    client = connect_mqtt(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    # Prepare datasource
    try:
        # generate_height_data('src/data/height.csv', 300)
        datasource = FileDatasource(
            "src/data/data.csv",
            "src/data/gps.csv",
            "src/data/height.csv",
        )
    except FileNotFoundError:
        # generate_height_data('data/height.csv', 300)
        datasource = FileDatasource(
            "data/data.csv",
            "data/gps.csv",
            "data/height.csv",
        )

    # Infinity publish data
    publish(client, MQTT_TOPIC, datasource, DELAY)


if __name__ == '__main__':
    run()
