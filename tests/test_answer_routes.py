from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_answer_route():

    response = client.post("/answers/evaluate",
    json={
    "question": "string",
    "answer": "stringlllllllllll",
    "level": "beginner"
    })

    assert response.status_code == 200

    data = responde.json()

    assert "score" in data
    assert "feedback" in data

    assert isinstance(data["score"], int)
    assert isinstance(data["feedback"], str)


