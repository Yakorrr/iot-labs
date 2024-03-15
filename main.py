from config import *
from models import ProcessedAgentData, ProcessedAgentDataInDB
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, WebSocket, WebSocketDisconnect,  HTTPException
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
# Insert data to database 
@app.post("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def create_processed_agent_data(data: List[ProcessedAgentData]):
    response_data = []

    with engine.connect() as connection:
        trans = connection.begin()
        try:
            for item in data:
                insert_dict = {
                    'road_state': item.road_state,
                    'x': item.agent_data.accelerometer.x,
                    'y': item.agent_data.accelerometer.y,
                    'z': item.agent_data.accelerometer.z,
                    'latitude': item.agent_data.gps.latitude,
                    'longitude': item.agent_data.gps.longitude,
                    'timestamp': item.agent_data.timestamp,
                }
                result = connection.execute(processed_agent_data.insert().values(insert_dict))
                inserted_id = result.inserted_primary_key[0]

                insert_dict['id'] = inserted_id
                response_data.append(insert_dict)
            
            trans.commit()
        except SQLAlchemyError as e:
            trans.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to insert data into the database: {e}")

    return [ProcessedAgentDataInDB(**item) for item in response_data]

# Get data by id 
@app.get("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def read_processed_agent_data(processed_agent_data_id: int):
    with engine.connect() as connection:
        select_query = select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)
        result = connection.execute(select_query).first()
        if result is None:
            raise HTTPException(status_code=404, detail="Data not found")
        return ProcessedAgentDataInDB(**result._asdict())

# Get list of data 
@app.get("/processed_agent_data/", response_model=List[ProcessedAgentDataInDB])
def list_processed_agent_data():
    with engine.connect() as connection:
        select_query = select(processed_agent_data)
        results = connection.execute(select_query).fetchall()
    return [ProcessedAgentDataInDB(**row._asdict()) for row in results]


# Update data 
@app.put("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def update_processed_agent_data(processed_agent_data_id: int, data: ProcessedAgentData):
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            update_query = processed_agent_data.update().where(processed_agent_data.c.id == processed_agent_data_id).values(
                road_state=data.road_state,
                x=data.agent_data.accelerometer.x,
                y=data.agent_data.accelerometer.y,
                z=data.agent_data.accelerometer.z,
                latitude=data.agent_data.gps.latitude,
                longitude=data.agent_data.gps.longitude,
                timestamp=data.agent_data.timestamp,
            )
            result = connection.execute(update_query)
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Data not found")
            trans.commit()
            
            select_query = select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)
            updated_row = connection.execute(select_query).first()
            return ProcessedAgentDataInDB(**updated_row._asdict())
        except SQLAlchemyError as e:
            trans.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to update data: {e}")

# Delete by id 
@app.delete("/processed_agent_data/{processed_agent_data_id}", response_model=ProcessedAgentDataInDB)
def delete_processed_agent_data(processed_agent_data_id: int):
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            select_query = select(processed_agent_data).where(processed_agent_data.c.id == processed_agent_data_id)
            record_to_delete = connection.execute(select_query).first()
            if record_to_delete is None:
                raise HTTPException(status_code=404, detail="Data not found")
            
            delete_query = processed_agent_data.delete().where(processed_agent_data.c.id == processed_agent_data_id)
            connection.execute(delete_query)
            trans.commit()
            return ProcessedAgentDataInDB(**record_to_delete._asdict())
        except SQLAlchemyError as e:
            trans.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to delete data: {e}")


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run(app, host="127.0.0.1", port=8000) 