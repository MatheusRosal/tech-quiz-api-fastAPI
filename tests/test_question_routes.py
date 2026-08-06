from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_question_service():
    response = client.post("/questions/generate", 
    json={
    "topic": "string",
    "level": "beginner"
    })

    assert response.status_code == 200

    data = response.json()

    assert data["topic"] == "string"
    assert data["level"] == "beginner"
    assert "question" in data
    assert isinstance(data["question"], str)


def test_question_service_invalid():
    response = client.post("/questions/generate",
    json = {
    "topic": "string",
    "level": "banana"
    })

    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "literal_error"