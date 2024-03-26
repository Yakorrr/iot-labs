import os


def try_parse(obj_type, value: str):
    try:
        return obj_type(value)
    except TypeError:
        return None


# Configuration for agent MQTT
MQTT_BROKER_HOST = os.environ.get("MQTT_BROKER_HOST") or "localhost"
MQTT_BROKER_PORT = try_parse(int, os.environ.get("MQTT_BROKER_PORT")) or 1883
MQTT_TOPIC = os.environ.get("MQTT_TOPIC") or "agent_data_topic"
# Configuration for hub MQTT
HUB_MQTT_BROKER_HOST = os.environ.get("HUB_MQTT_BROKER_HOST") or "localhost"
HUB_MQTT_BROKER_PORT = try_parse(int, os.environ.get("HUB_MQTT_BROKER_PORT")) or 1883
HUB_MQTT_TOPIC = os.environ.get("HUB_MQTT_TOPIC") or "processed_agent_data_topic"
# Configuration for hub HTTP
HUB_HOST = os.environ.get("HUB_HOST") or "localhost"
HUB_PORT = try_parse(int, os.environ.get("HUB_PORT")) or 8000
HUB_URL = f"http://{HUB_HOST}:{HUB_PORT}"
