"""Database connection module."""

import psycopg2
from psycopg2.extras import RealDictCursor
import logging
from fastapi import HTTPException

"""
TODO: remove hardcoded credentials
add indexes?
use simpleconnectionpool to avoid creating a new connection in each request
"""

def get_connection():
    try:
        db = psycopg2.connect(
        host="localhost",
        database="earthquakes",
        user="eq_user",
        password="password",
        cursor_factory=RealDictCursor
        )
        return db
    except psycopg2.Error as e:
        logging.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=500, detail="Database connection error")