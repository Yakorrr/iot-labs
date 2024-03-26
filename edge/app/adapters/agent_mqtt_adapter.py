import logging

import paho.mqtt.client as mqtt_client
from app.interfaces.agent_gateway import AgentGateway
from app.entities.agent_data import AgentData
from app.usecases.data_processing import process_agent_data


class AgentMQTTAdapter(AgentGateway):
    def __init__(self, broker_host, broker_port, topic, hub_gateway, batch_size=10):
        self.batch_size = batch_size
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.topic = topic
        self.hub_gateway = hub_gateway
        self.client = mqtt_client.Client()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logging.info("Connected to agent.")
            self.client.subscribe(self.topic)
        else:
            logging.info(f"Failed to connect to agent with return code {rc}.")

    def on_message(self, client, userdata, msg):
        """
        Method to handle incoming messages from the agent.
        Parameters:
        client: MQTT client instance.
        userdata: Any additional user data passed to the MQTT client.
        msg: The MQTT message received from the agent.
        """
        try:
            logging.info(f"MESSAGE: {msg.topic} {msg.payload}")
            payload: str = msg.payload.decode("utf-8")
            agent_data = AgentData.model_validate_json(payload, strict=True)
            data = process_agent_data(agent_data)
            if not self.hub_gateway.save_data(data):
                logging.error("Failed to save data to the hub.")
        except Exception as e:
            logging.error(f"Error processing message: {e}")

    def connect(self):
        """
        Method to establish a connection to the agent.
        """
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_host, self.broker_port, 60)

    def start(self):
        """
        Method to start listening for messages from the agent.
        """
        self.client.loop_start()

    def stop(self):
        """
        Method to stop the agent gateway and clean up resources.
        """
        self.client.loop_stop()
