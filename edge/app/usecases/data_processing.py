import logging

from app.entities.agent_data import AgentData
from app.entities.processed_agent_data import ProcessedAgentData

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output log messages to the console
        logging.FileHandler("app.log"),  # Save log messages to a file
    ],
)

def process_agent_data(agent_data: AgentData, ) -> ProcessedAgentData:
    """
    Process agent data and classify the state of the road surface.
    Parameters:
    agent_data (AgentData): Agent data that contains accelerometer, GPS, and timestamp.
    Returns:
    processed_data (ProcessedAgentData): Processed data containing the classified state of
    the road surface and agent data.
    """
    smoothness = agent_data.accelerometer.z - (agent_data.height.height * 12000)
    logging.info(f"Smoothness: {smoothness}")
    if smoothness > 13000:
        road_state = "bumpy"
    elif smoothness < -8000:
        road_state = "pothole"
    else:
        road_state = "smooth"

    return ProcessedAgentData(road_state=road_state, agent_data=agent_data)
