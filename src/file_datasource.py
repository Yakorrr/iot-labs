from dataclasses import dataclass
from csv import reader
from datetime import datetime
from src.domain.accelerometer import Accelerometer
from src.domain.gps import Gps
from src.domain.aggregated_data import AggregatedData


@dataclass
class FileDatasource:
    def __init__(
            self,
            accelerometer_filename: str,
            gps_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.accelerometer_file = None
        self.gps_file = None
        self.accelerometer_reader = None
        self.gps_reader = None

    def read(self) -> AggregatedData:
        """Method returns data received from sensors"""
        if not self.accelerometer_file or not self.gps_file:
            raise RuntimeError("Files are not opened. Call start_reading() first.")

        accelerometer_data = self._read_next_accelerometer_data()
        gps_data = self._read_next_gps_data()
        current_time = datetime.now()

        return AggregatedData(accelerometer_data, gps_data, current_time)

    def _read_next_accelerometer_data(self) -> Accelerometer:
        while True:
            row = next(self.accelerometer_reader, None)  # Use None to handle end of file

            if row is None:  # End of file reached, reset file pointer
                self.accelerometer_file.seek(0)
                continue

            if row[0].isdigit():
                break

        # Assuming the structure of accelerometer data in CSV is [x, y, z]
        return Accelerometer(int(row[0]), int(row[1]), int(row[2]))

    def _read_next_gps_data(self) -> Gps:
        while True:
            row = next(self.gps_reader, None)  # Use None to handle end of file

            if row is None:  # End of file reached, reset file pointer
                self.gps_file.seek(0)
                continue

            if row[0].replace('.', '', 1).isdigit():
                break

        # Assuming the structure of GPS data in CSV is [longitude, latitude]
        return Gps(float(row[0]), float(row[1]))

    def start_reading(self):
        """The method must be called before starting to read data"""

        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.accelerometer_reader = reader(self.accelerometer_file)
        self.gps_reader = reader(self.gps_file)

    def stop_reading(self):
        """The method must be called to finish reading the data"""
        if self.accelerometer_file:
            self.accelerometer_file.close()

        if self.gps_file:
            self.gps_file.close()

        # Reset file pointers for the next iteration
        self.accelerometer_file = None
        self.gps_file = None
        self.accelerometer_reader = None
        self.gps_reader = None
