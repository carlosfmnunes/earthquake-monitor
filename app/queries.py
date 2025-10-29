"""SQL queries for accessing earthquake data"""

from typing import Optional
from app.database import get_connection
from app.schemas import EarthquakeCreate
import logging
from fastapi import HTTPException
from datetime import datetime

# TODO: check datetime, string format etc in queries


def list_earthquakes(
    min_magnitude: Optional[float] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 20,
    offset: int = 0,
):
    """Return the list of earthquakes in the database"""
    db = cur = None
    try:
        db = get_connection()
        cur = db.cursor()

        query = "SELECT * FROM earthquakes WHERE 1=1"
        params = []

        if min_magnitude is not None:
            query += " AND magnitude >= %s"
            params.append(min_magnitude)

        if start_time is not None:
            query += " AND time >= %s"
            params.append(start_time)

        if end_time is not None:
            query += " AND time <= %s"
            params.append(end_time)

        query += " ORDER BY time DESC LIMIT %s OFFSET %s;"
        params.extend([limit, offset])

        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        return rows

    except Exception as e:
        logging.exception("Error getting earthquakes")
        raise HTTPException(status_code=500, detail="Query failed")
    finally:
        if cur:
            cur.close()
        if db:
            db.close()


def get_earthquake_details(id: int):
    """
    Return the details of an earthquake stored in the database with a specific id, if existent
    """
    db = cur = None
    try:
        db = get_connection()
        cur = db.cursor()
        cur.execute("SELECT * from earthquakes WHERE id = %s", (id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Earthquake not found")
        return row

    except Exception as e:
        logging.exception("Error getting earthquakes")
        raise HTTPException(status_code=500, detail="Query failed")
    finally:
        if cur:
            cur.close()
        if db:
            db.close()


def add_earthquake(eq: EarthquakeCreate):
    """Publish a new earthquake entry to the database"""
    db = cur = None
    try:
        db = get_connection()
        cur = db.cursor()
        cur.execute(
            """
            INSERT INTO earthquakes (location, magnitude, depth, time)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """,
            (eq.location, eq.magnitude, eq.depth, eq.time),
        )
        new_row = cur.fetchone()
        db.commit()
        return new_row

    except Exception as e:
        logging.error(f"Error inserting earthquake: {e}")
        raise HTTPException(status_code=500, detail="Failed to insert earthquake")
    finally:
        if cur:
            cur.close()
        if db:
            db.close()
