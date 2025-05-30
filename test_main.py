from fastapi.testclient import TestClient   #This whole thing is for unit testing
from main import app

client=TestClient(app)

def test_create_task():
    response=client.post("/tasks",json={"title":"Test task"})
    assert response.status_code==200
    assert response.json()["title"]=="Test task"
    assert response.json()["done"]==False