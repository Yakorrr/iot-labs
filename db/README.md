# iot-labs

# Lab 2

to start:

1. Activate Environment: source ./venv/bin/activate # linux or .\venv\Scripts\activate.bat # windows
2. cd docker
3. docker-compose up --build or docker compose up --build (if docker desktop version)

connect to pgadmin:

1. run container
2. localhost:5050
3. email: admin@admin.com
4. password: root
5. go to Server -> test_db -> Schemas -> Tables -> processed_agent_data;

see endpoints:

1. run container
2. http://127.0.0.1:8000/docs
3. There is 5 CRUD endpoints

you can find endpoints in main.py
also subscription logic("логіку підписки на оволення даних") is in main.py
