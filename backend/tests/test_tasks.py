import os
import pytest
from fastapi.testclient import TestClient
from jose import jwt
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from app.main import app
from app.db import get_session
from app.models import Task

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "test-secret-key")

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def create_test_token(user_id: str) -> str:
    payload = {"sub": user_id}
    token = jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")
    return token


def test_create_task(client: TestClient):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/user123/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["user_id"] == "user123"
    assert data["status"] == "open"


def test_list_tasks(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task1 = Task(user_id="user123", title="Task 1", status="open")
    task2 = Task(user_id="user123", title="Task 2", status="done")
    task3 = Task(user_id="user456", title="Task 3", status="open")

    session.add(task1)
    session.add(task2)
    session.add(task3)
    session.commit()

    response = client.get("/api/user123/tasks", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all(task["user_id"] == "user123" for task in data)


def test_list_tasks_with_filters(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task1 = Task(user_id="user123", title="Task 1", status="open", priority="high")
    task2 = Task(user_id="user123", title="Task 2", status="done", priority="low")

    session.add(task1)
    session.add(task2)
    session.commit()

    response = client.get("/api/user123/tasks?status=open", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "open"

    response = client.get("/api/user123/tasks?priority=high", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["priority"] == "high"


def test_list_tasks_with_search(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task1 = Task(user_id="user123", title="Buy groceries", description="Milk and eggs")
    task2 = Task(user_id="user123", title="Call plumber", description="Fix sink")

    session.add(task1)
    session.add(task2)
    session.commit()

    response = client.get("/api/user123/tasks?q=groceries", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "groceries" in data[0]["title"]


def test_get_task(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task = Task(user_id="user123", title="Test Task")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.get(f"/api/user123/tasks/{task.id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Test Task"


def test_update_task(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task = Task(user_id="user123", title="Old Title")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.put(
        f"/api/user123/tasks/{task.id}",
        json={"title": "New Title", "priority": "high"},
        headers=headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New Title"
    assert data["priority"] == "high"


def test_delete_task(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task = Task(user_id="user123", title="To Delete")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.delete(f"/api/user123/tasks/{task.id}", headers=headers)
    assert response.status_code == 204

    response = client.get(f"/api/user123/tasks/{task.id}", headers=headers)
    assert response.status_code == 404


def test_toggle_task_completion(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task = Task(user_id="user123", title="Test Task", status="open")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.patch(f"/api/user123/tasks/{task.id}/complete", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "done"

    response = client.patch(f"/api/user123/tasks/{task.id}/complete", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "open"


def test_unauthorized_access(client: TestClient):
    response = client.get("/api/user123/tasks")
    assert response.status_code == 403


def test_forbidden_user_access(client: TestClient, session: Session):
    token = create_test_token("user123")
    headers = {"Authorization": f"Bearer {token}"}

    task = Task(user_id="user456", title="Other User Task")
    session.add(task)
    session.commit()
    session.refresh(task)

    response = client.get(f"/api/user456/tasks", headers=headers)
    assert response.status_code == 403
