from config import *
from models import ProcessedAgentData, ProcessedAgentDataInDB
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,  HTTPException, Path
from typing import Set, List
import json


# SQLAlchemy setup 
DATABASE_URL =  f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL) 
metadata = MetaData() 

# Define the ProcessedAgentData table
processed_agent_data = Table(
    "processed_agent_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("road_state", String),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("timestamp", DateTime),
)

app = FastAPI()

subscriptions: Set[WebSocket] = set()

@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    subscriptions.add(websocket)
    try:
        while True:
            # Here, we just receive messages and keep the connection open.
            # You might want to process the received messages in some way.
            await websocket.receive_text()
    except WebSocketDisconnect:
        subscriptions.remove(websocket)

async def send_data_to_subscribers(data):
    for websocket in subscriptions:
        # Convert the data to JSON and send it to all connected WebSocket clients
        await websocket.send_json(json.dumps(data))


# FastAPI CRUDL endpoints 

# Send data to subscribers 
@app.post("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
async def create_processed_agent_data(data: List[ProcessedAgentData]):
    # Insert data into the database
    # Send data to subscribers
    # This function is asynchronous
    pass

# Get data by id 
@app.get("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int):
    # Get data by id from the database
    # This is a synchronous function
    pass

# Get list of data 
@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def list_processed_agent_data():
    # Get list of all processed agent data from the database
    # This is a synchronous function
    pass

# Update data 
@app.put("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    # Update processed agent data by id in the database
    # This is a synchronous function
    pass

# Delete by id 
@app.delete("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int):
    # Delete processed agent data by id from the database
    # This is a synchronous function
    pass


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="127.0.0.1", port=8000) 