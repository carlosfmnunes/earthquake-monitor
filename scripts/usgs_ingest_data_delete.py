import requests
from datetime import datetime
import logging
from app.database import get_connection

# logging
logging.basicConfig(
    filename="logs/ingest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def fetch_usgs_earthquakes(limit=10, last_fetch_time=datetime.timezone.utc()):
    """Fetch recent earthquakes from USGS GeoJSON API"""
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    params = {
        "format": "geojson",
        "limit": limit,
        "orderby": "time",
        "starttime": last_fetch_time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()["features"]
        logging.info(f"Fetched {len(data)} records from USGS")
        return data

    except Exception as e:
        logging.error(f"Error fetching data from USGS API: {e}")
        return []


def insert_earthquakes(data):
    db = cur = None
    try:
        db = get_connection()
        cur = db.cursor()

        inserted = 0

        for eq in data:
            try:
                props = eq["properties"]
                coords = eq["geometry"]["coordinates"]
                eq_time = datetime.fromtimestamp(props["time"] / 1000.0)

                cur.execute(
                    """
                    INSERT INTO earthquakes (location, magnitude, depth, time)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (props["place"], props["mag"], coords[2], eq_time),
                )
                inserted += 1

            except Exception as e:
                logging.error(
                    f"Failed to insert earthquake {props.get('place', 'unknown')}: {e}"
                )

        db.commit()
        logging.info(f"Inserted {inserted} records into the database.")

    except Exception as e:
        logging.error(f"Database error: {e}")

    finally:
        if cur:
            cur.close()
        if db:
            db.close()


def main():
    while True:
        data = fetch_usgs_earthquakes(limit=10, last_fetch_time=datetime.timezone.utc())
        if data:
            insert_earthquakes(data)
        else:
            logging.info("No data fetched.")


if __name__ == "__main__":
    main()
