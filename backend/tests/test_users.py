# backend/tests/test_users.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import Base, engine, SessionLocal

client = TestClient(app)

# DB를 테스트 모드로 초기화 (테스트 전후에 실행하면 좋습니다)
@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_user():
    response = client.post("/api/users/", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "user_id" in data

def test_read_users():
    response = client.get("/api/users/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
