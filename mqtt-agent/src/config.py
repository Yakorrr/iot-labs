import os


def try_parse(obj_type, value: str):
    try:
        return obj_type(value)
    except TypeError:
        return None


# MQTT config
MQTT_BROKER_HOST = os.environ.get('MQTT_BROKER_HOST') or 'localhost'
MQTT_BROKER_PORT = try_parse(int, os.environ.get('MQTT_BROKER_PORT')) or 1883
MQTT_TOPIC = os.environ.get('MQTT_TOPIC') or 'agent_data_topic'

# Delay for sending data to mqtt-agent in seconds
DELAY = try_parse(float, os.environ.get('DELAY')) or 0.1
