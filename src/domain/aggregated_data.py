from dataclasses import dataclass
from datetime import datetime
from src.domain.accelerometer import Accelerometer
from src.domain.gps import Gps
from src.domain.height import Height


@dataclass
class AggregatedData:
    accelerometer: Accelerometer
    gps: Gps
    height: Height
    time: datetime
