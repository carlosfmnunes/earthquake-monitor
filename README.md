## Earthquake Monitoring API

A simple FastAPI backend service for monitoring data from natural disasters. It ingests earthquake information from mock data, stores it in PostgreSQL and exposes it via REST API.

## Features:
- REST API built with FastAPI
- Data stored in PostgreSQL
- Endpoints to:
  - List latest earthquakes with pagination, with magnitude and date range filters
  - Fetch specific earthquake details by ID
  - Insert earthquake data
- Mock data ingestion script to simulate live updates

## Setup Instructions:
### 1. Clone the repo:
```bash
git clone https://github.com/carlosfmnunes/earthquake-monitor.git
cd earthquake-monitor
```

### 2. Create and activate a virtual environment (venv)
Windows:  
```bash
python -m venv venv  
venv\Scripts\activate
```
macOS/Linux:

```bash
python3 -m venv venv  
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```


### 4. Start PostgreSQL locally
Make sure service is running (port 5432).
Create database and user:  
```bash
CREATE DATABASE earthquakes;  
CREATE USER eq_user WITH PASSWORD 'password';  
GRANT ALL PRIVILEGES ON DATABASE earthquakes TO eq_user;
\c earthquakes  
GRANT ALL ON SCHEMA public TO eq_user;  
ALTER SCHEMA public OWNER TO eq_user;
```



### 5. Initialize database schema
```bash
python -m scripts.init_db.py
```


### 6. (Optional) Add unique constraint to prevent duplicate entries log outputs
```bash
ALTER TABLE earthquakes  
ADD CONSTRAINT unique_eq UNIQUE (location, time);
```


### 7. (Optional) Ingest mock data:
```bash
python -m scripts.ingest_mock_data.py
```


### 8. Run FastAPI app
```bash
uvicorn app.main:app --reload
```


API avaiable at: http://127.0.0.1:8000  
Swagger docs: http://127.0.0.1:8000/docs

## Design decisions:
- Pydantic models EarthquakeCreate and EarthquakeRead for separate input/output schemas  
- Request logging implemented via middleware  
- PostgreSQL storage  
- SQL queries isolated in queries.py for maintainability  

## Improvements (Future Work)
- Use connection pooling  
- Replace hardcoded DB credentials with environment variables  
- Implement real USGS API ingestion  
