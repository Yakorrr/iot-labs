import csv
import random


def generate_height_data(filename, num_rows):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['height'])  # Write header

        for _ in range(num_rows):
            height = round(random.uniform(0.1, 2.0), 3)  # Generate random height between 0.5 and 2.0 meters
            writer.writerow([height])
