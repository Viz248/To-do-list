from fastapi.testclient import TestClient   #This whole thing is for unit testing
from main import app

client=TestClient(app)

def test_create_task():
    response=client.post("/tasks/tasks",json={"title":"Test task"})
    assert response.status_code==200
    assert response.json()["title"]=="Test task"
    assert response.json()["done"]==False

def test_create_task_missing_fields():
    response=client.post("/tasks/tasks",json={})
    assert response.status_code==422

def test_create_task_invalid_type():
    response=client.post("/tasks/tasks",json={"title":123})
    assert response.status_code==422

def test_update_task():
    response=client.post("/tasks/tasks",json={"title":"Test task"})
    patch_response=client.patch("/tasks/tasks/1",json={"title":"Updated Test task"})
    assert patch_response.status_code==200
    assert patch_response.json()["title"]=="Updated Test task"
    assert patch_response.json()["done"]==False