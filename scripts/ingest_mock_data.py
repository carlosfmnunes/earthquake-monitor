"""Script to ingest mock earthquake data periodically"""

import time
import logging
from app import queries
from sample_data import earthquake_records
from app.schemas import EarthquakeCreate


logging.basicConfig(
    filename="logs/ingest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

while True:
    for eq in earthquake_records:
        eq_obj = EarthquakeCreate(**eq)
        try:
            queries.add_earthquake(eq_obj)
            logging.info(f"Inserted earthquake: {eq_obj.location}, {eq_obj.magnitude}")
        except Exception as e:
            logging.error(f"Failed to insert earthquake record: {e}")
    time.sleep(10)
