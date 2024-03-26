from app.entities.processed_agent_data import ProcessedAgentData
from app.interfaces.hub_gateway import HubGateway
from paho.mqtt import client as mqtt_client


class HubMqttAdapter(HubGateway):
    def __init__(self, broker, port, topic):
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = self._connect_mqtt(broker, port)

    def save_data(self, processed_data: ProcessedAgentData):
        """
        Method to save the processed agent data in the database.
        Parameters:
            processed_data (ProcessedAgentData): The processed agent data to be saved.
        Returns:
            bool: True if the data is successfully saved, False otherwise.
        """
        # Connect to the broker
        msg = processed_data.model_dump_json()
        result = self.mqtt_client.publish(self.topic, msg)
        status = result[0]
        if status == 0:
            return True
        else:
            print(f"Failed to send message to topic {self.topic}")
            return False

    @staticmethod
    def _connect_mqtt(broker, port):
        """Create MQTT client"""
        print(f"CONNECT TO {broker}:{port}")

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print(f"Connected to MQTT Broker ({broker}:{port})!")
            else:
                print("Failed to connect {broker}:{port}, return code %d\n", rc)
                exit(rc)  # Stop execution

        client = mqtt_client.Client()
        client.on_connect = on_connect
        client.connect(broker, port)
        client.loop_start()
        return client
