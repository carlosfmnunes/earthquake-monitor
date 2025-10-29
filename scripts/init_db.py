"""Script to initialize the earthquake database and create tables if they don't exist."""

from app.database import get_connection
import logging

logging.basicConfig(level=logging.INFO)


def init_db():
    db = cur = None
    try:
        db = get_connection()
        cur = db.cursor()

        cur.execute(
            """
        CREATE TABLE IF NOT EXISTS earthquakes (
            id SERIAL PRIMARY KEY,
            location TEXT NOT NULL,
            magnitude FLOAT NOT NULL,
            depth FLOAT NOT NULL,
            time TIMESTAMP NOT NULL,
            UNIQUE(location, time)
        );
        """
        )

        db.commit()
        logging.info("Database initialized successfully")

    except Exception as e:
        logging.error(f"Database initialization failed: {e}")

    finally:
        if cur:
            cur.close()
        if db:
            db.close()


if __name__ == "__main__":
    init_db()
