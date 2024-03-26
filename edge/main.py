import logging

from app.adapters.agent_mqtt_adapter import AgentMQTTAdapter
from app.adapters.hub_http_adapter import HubHttpAdapter

from config import (
    HUB_URL,
    MQTT_BROKER_HOST,
    MQTT_BROKER_PORT,
    MQTT_TOPIC,
)


if __name__ == "__main__":
    # Configure logging settings
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
        handlers=[
            logging.StreamHandler(),  # Output log messages to the console
            logging.FileHandler("app.log"),  # Save log messages to a file
        ],
    )

    # Create an instance of the HubHTTPAdapter using the configuration
    hub_adapter = HubHttpAdapter(
        api_base_url=HUB_URL,
    )

    # Create an instance of the AgentMQTTAdapter using the configuration
    agent_adapter = AgentMQTTAdapter(
        broker_host=MQTT_BROKER_HOST,
        broker_port=MQTT_BROKER_PORT,
        topic=MQTT_TOPIC,
        hub_gateway=hub_adapter,
    )

    try:
        # Connect to the MQTT broker and start listening for messages
        agent_adapter.connect()
        agent_adapter.start()
        # Keep the system running indefinitely
        while True:
            pass
    except KeyboardInterrupt:
        # Stop the MQTT adapter and exit gracefully if interrupted by the user
        agent_adapter.stop()
        logging.info("System stopped.")
