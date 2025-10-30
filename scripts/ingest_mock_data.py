"""Script to ingest mock earthquake data periodically."""

import time
import logging
import importlib
import sample_data
from app import queries
from app.schemas import EarthquakeCreate

logging.basicConfig(
    filename="logs/ingest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

while True:
    importlib.reload(sample_data)
    earthquake_records = sample_data.earthquake_records

    new_inserts = 0

    for eq in earthquake_records:
        eq_obj = EarthquakeCreate(**eq)
        try:
            result = queries.add_earthquake(eq_obj)
            if result:
                new_inserts += 1
                logging.info(f"Inserted new earthquake: {eq_obj.location}, {eq_obj.magnitude}")
        except Exception as e:
            logging.error(f"Failed to insert earthquake record: {e}")

    if new_inserts == 0:
        logging.info("No new earthquake records to insert in this cycle.")
    time.sleep(10)
