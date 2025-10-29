"""FastAPI application for Earthquake Monitoring"""

from fastapi import FastAPI, HTTPException, Request
from typing import Optional
from app.schemas import *
import logging
import time
from app import queries

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
    filename="logs/app.log",
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
async def log_requests(request: Request, call_next): ## TODO: check async or not
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
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
):
    try:
        rows = queries.list_earthquakes(
            min_magnitude, start_time, end_time, limit, offset
        )
        return rows
    except Exception:
        logging.exception("Error getting earthquakes")
        raise HTTPException(status_code=500, detail="Query failed")


@app.get(
    "/earthquakes/{id}/",
    response_model=EarthquakeRead,
    summary="Get specific earthquake details",
    description="Fetch information about a earthquake by its ID.",
)
def get_earthquake_details(id: int):
    try:
        row = queries.get_earthquake_details(id)
        if not row:
            raise HTTPException(status_code=404, detail="Earthquake not found")
        return row
    except Exception:
        logging.exception("Error getting earthquake")
        raise HTTPException(status_code=500, detail="Query failed")


@app.post(
    "/earthquakes/",
    summary="Add a new earthquake",
    description="Insert a new earthquake record in the database.",
    response_model=EarthquakeRead,
)
def add_earthquake(eq: EarthquakeCreate):
    try:
        new_row = queries.add_earthquake(eq)
        return new_row
    except Exception as e:
        logging.error(f"Error inserting earthquake: {e}")
        raise HTTPException(status_code=500, detail="Failed to insert earthquake")


## TODO: add running script to fetch data from external API periodically
## dockerize the app and the database
## update env variables and remove hardcoded credentials