from fastapi.testclient import TestClient
from good.a2a_server.app import app

client = TestClient(app)


def test_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from good a2a_server!"}
