# IoT PROJECT
### TEAM-12

----
## Description
_A comprehensive system for monitoring and analyzing the condition of the road surface_

---
## Overview
The system includes a device on the machine (stm32), edge devices, cloud.
The system includes the following parts:
- Data acquisition module (Agent) - an agent service on the machine that takes sensor readings and sends them to the server


- Edge Data Logic module - a service that deals with the primary processing of data, in our case, determines the state of the road surface and sends the analyzed data to the Hub


- Data storage module (Hub) - a service that deals with preprocessing of the data received from the Agent and further storage of the processed data in the database

  
- Store is an api for receiving and storing data in the database


- [Next stage] Visualization module (Accelerometer UI, Map UI) - an interface for visualization (monitoring) of system results

---

## Installation

Make sure you have [Python](https://www.python.org/) installed (this project uses python version 3.9) and [Docker Desktop](https://www.docker.com/products/docker-desktop/). 
In addition, you can also download [MQTT Explorer](https://mqtt-explorer.com) to view visualized graphs of sensor data in real time

From your command line:

#### Clone this repository
```
git clone https://github.com/Yakorrr/iot-labs.git
```
#### Go into the repository
```
cd iot-labs
```

## Usage

#### To start a project run next commands:

Go to docker folder
``` 
cd docker/
```
Build docker
```commandline
docker-compose up --build
```

In logs, you can see that all data transferred from Agent to Edge-->Hub and successfully saved to Store. Also, you can open MQTT Explorer and see real time graphs.
To connect to mqtt broker:
1. Create a new connection
2. Enter any name
3. Protocol must be `mqtt://`
4. Host must be `localhost`
5. Port `1883`

#### Go to different places, check if everything is working correctly
You can see what data was transferred: open http://localhost:8000/processed_agent_data/ –
There will be all processed data in json format

Open http://localhost:5050 and there will be loging page of pgAdmin.
By default, the login details are as follows:
- login: `admin@admin.com`
- password: `root`

To connect to Postgres database follow these steps:
1. Sign in to the pgAdmin
2. Right click on `Servers` select `Register`
3. In opened window fill in the required fields:
    - In `General Tab` in the Name field, type `Store`
    - In `Connection Tab`:
      - Host name/address = `postgres_db`
      - Maintenance database = `test_db`
      - Username = `user`
      - Password = `pass`
    - Click `Save` button
4. Expand Server panel and go to `Servers -> Store -> Databases -> test_db -> Schemas -> Tables -> processed_agent_data`
5. Right click on `processed_agent_data` table and select `Query tool`. In editor type 
```
SELECT * FROM processed_agent_data
```
and you will see all data records

The last link you can follow is http://localhost:8000/docs – It is FastAPI with all necessary CRUD API Endpoints

All settings above you can change in `docker-compose.yaml` and in `agent/src/config.py`(for MQTT) `store/src/config.py`(for postgres_db, pgadmin, store)
