Earthquake Monitoring API

A simple FastAPI backend service for monitoring data from natural disasters. It ingests earthquake information from mock data, stores it in PostgreSQL and exposes it via REST API.

## Features:
- REST API built with FastAPI
- Data stored in PostgreSQL
- Listing of recent earthquakes, filtering by magnitude and date range
- Fetching specific earthquake details by ID
- Mock data ingestion script to simulate live updates

## Setup:
- Clone the repo:
git clone https://github.com/carlosfmnunes/earthquake-monitor.git
cd earthquake-monitor

- Create and activate a virtual environment (venv)
python -m venv venv
venv\Scripts\activate # Windows
# or
source venv/bin/activate # macOS/Linux

## Install dependencies
pip install -r requirements.txt

## Start PostgreSQL locally
Make sure service is running (port 5432)
If needed, create database and user:
CREATE DATABASE earthquakes;
CREATE USER eq_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE earthquakes TO eq_user;

## Initialize database schema
python scripts/init_db.py

## (Optional) Ingest mock data:
python scripts/ingest_mock_data.py

## Run FastAPI app
uvicorn app.main:app --reload

API avaiable at: http://127.0.0.1:8000
Swagger docs: http://127.0.0.1:8000/docs

## Design decisions:
Pydantic models EarthquakeCreate and EarthquakeRead for separate input/output schemas
Request logging implemented via middleware
PostgreSQL storage
SQL queries isolated in queries.py for maintainability

## Improvements (Future Work)
Use connection pooling
Replace hardcoded DB credentials with environment variables
Implement real USGS API ingestion