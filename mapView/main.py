import asyncio
import json
import logging
import threading
from kivy.app import App
from kivy_garden.mapview import MapView, MapMarker
from websockets import connect
from lineMapLayer import LineMapLayer
from kivy.clock import Clock
from queue import Queue

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s",
    handlers=[
        logging.StreamHandler(),  # Output log messages to the console
        logging.FileHandler("app.log"),  # Save log messages to a file
    ],
)

class CarMarker(MapMarker):
    def __init__(self, **kwargs):
        super().__init__(source="images/car.png", **kwargs)

class MapViewApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mapview = MapView(zoom=12, lat=50.44155890642017, lon=30.56055307388306)
        self.line_layer = LineMapLayer()
        self.car_marker = None
        self.mapview.add_layer(self.line_layer)
        self.websocket_url = "ws://localhost:8000/ws/"
        self.data_queue = Queue()

    def build(self):
        return self.mapview

    async def websocket_client(self):
        async with connect(self.websocket_url) as websocket:
            await websocket.send("connect")
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                logging.info(f"Received {data}")
                self.data_queue.put(data)

    def start_websocket_client(self):
        asyncio.run(self.websocket_client())

    def update_map(self, dt):
        if not self.data_queue.empty():
            data = self.data_queue.get()
            jsonData = json.loads(data)
            longitude = jsonData['agent_data']['gps']['longitude']
            latitude = jsonData['agent_data']['gps']['latitude']
            road_state = jsonData['road_state']
            self.line_layer.add_point((longitude, latitude))
            if (self.car_marker is not None):
                self.car_marker.canvas.clear()
            self.car_marker = CarMarker(lat=longitude, lon=latitude)
            self.mapview.add_widget(self.car_marker)
            if (road_state == 'smooth'):
                logging.info(f"Adding smooth marker at {latitude}, {longitude}")
                self.mapview.add_marker(MapMarker(lat=longitude, lon=latitude, source='images/smooth.png'))
            if (road_state == 'bumpy'):
                logging.info(f"Adding pothole marker at {latitude}, {longitude}")
                self.mapview.add_marker(MapMarker(lat=longitude, lon=latitude, source='images/bump.png'))
            if (road_state == 'pothole'):
                logging.info(f"Adding pothole marker at {latitude}, {longitude}")
                self.mapview.add_marker(MapMarker(lat=longitude, lon=latitude, source='images/pothole.png'))

    def on_start(self):
        # Запускаємо асинхронний клієнт у фоновому потоці
        threading.Thread(target=self.start_websocket_client, daemon=True).start()
        # Регулярно оновлюємо карту
        Clock.schedule_interval(self.update_map, 1)

if __name__ == "__main__":
    MapViewApp().run()
