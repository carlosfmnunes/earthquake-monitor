from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_earthquakes():
    response = client.get("/earthquakes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
