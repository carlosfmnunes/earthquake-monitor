from pydantic import BaseModel
from datetime import datetime

class EarthquakeCreate(BaseModel):
    location: str
    magnitude: float
    depth: float
    time: datetime

class EarthquakeRead(EarthquakeCreate):
    id: int
