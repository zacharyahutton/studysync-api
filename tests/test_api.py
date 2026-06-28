import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def auth_header(client: TestClient, email: str = "student@example.com", password: str = "password123") -> dict[str, str]:
    client.post("/auth/register", json={"email": email, "password": password})
    login = client.post("/auth/login", json={"email": email, "password": password})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_register_and_login(client: TestClient):
    res = client.post("/auth/register", json={"email": "a@test.com", "password": "password123"})
    assert res.status_code == 201
    login = client.post("/auth/login", json={"email": "a@test.com", "password": "password123"})
    assert login.status_code == 200
    assert "access_token" in login.json()


def test_deadline_requires_auth(client: TestClient):
    res = client.get("/deadlines")
    assert res.status_code == 401


def test_create_course_and_deadline(client: TestClient):
    headers = auth_header(client)
    course = client.post("/courses", json={"name": "Algorithms", "code": "CS201"}, headers=headers)
    assert course.status_code == 201
    course_id = course.json()["id"]
    due = datetime(2026, 12, 1, 17, 0, tzinfo=timezone.utc).isoformat()
    deadline = client.post(
        "/deadlines",
        json={"course_id": course_id, "title": "Final project", "due": due},
        headers=headers,
    )
    assert deadline.status_code == 201
    listed = client.get("/deadlines", headers=headers)
    assert len(listed.json()) == 1
