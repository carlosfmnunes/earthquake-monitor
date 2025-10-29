from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from app.database import get_connection
from app.schemas import *
import logging
import time

app = FastAPI(
    title="Earthquake Monitoring API",
    description="""
    REST API for managing earthquake data globally.

    ** Features:**
    - Fetch all earthquakes
    - Filter by magnitude and date
    - Insert new eartquake entry
    """,
    version="1.0.0",
)

logging.basicConfig(
    filename="app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

""" data_records = {
    1: {
        "id": 1,
        "location": "Portugal",
        "magnitude": 5.5,
        "depth": 322.7,
        "time": "2025-10-26T18:51:46.150789"
    },
    2: {
        "id": 2,
        "location": "Spain",
        "magnitude": 3.5,
        "depth": 352.1,
        "time": "2025-10-27T18:10:46.150789"
    },
    3: {
        "id": 3,
        "location": "Portugal",
        "magnitude": 3.5,
        "depth": 539.1,
        "time": "2025-10-28T12:51:46.150789"
    }
} """


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware to log all API requests"""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logging.info(
        f"{request.method} {request.url.path} status={response.status_code} time={duration:.3f}s"
    )
    return response


@app.get("/")
def index():
    """Root endpoint with simple status message"""
    return {"message": "Welcome, Earthquake Monitoring API service is running."}


@app.get("/health/")
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "ok"}


@app.get(
    "/earthquakes/",
    summary="List earthquakes",
    description="Returns all earthquakes, with optional filtering by magnitude and date range.",
    response_model=list[EarthquakeRead],
)
def get_earthquakes(
    min_magnitude: Optional[float] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 20,
    offset: int = 0,
):
    """Return the list of earthquakes in the database"""
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
        cur.close()
        db.close()


@app.get(
    "/earthquakes/{id}/",
    response_model=EarthquakeRead,
    summary="Get specific earthquake details",
    description="Fetch information about a earthquake by its ID.",
)
def get_earthquake_details(id: int):
    """
    Return the details of an earthquake stored in the database with a specific id, if existent
    """
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
        cur.close()
        db.close()


@app.post(
    "/earthquakes/",
    summary="Add a new earthquake",
    description="Insert a new earthquake record in the database.",
    response_model=EarthquakeRead,
)
def add_earthquake(eq: EarthquakeCreate):
    """Publish a new earthquake entry to the database"""
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
        cur.close()
        db.close()
