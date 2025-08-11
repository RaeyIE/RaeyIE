from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_suggest_okrs():
    payload = {
        "team": "Growth",
        "period": "Q3 2025",
        "context": "Focus on activation and retention",
    }
    response = client.post("/suggest_okrs", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "objectives" in data
    assert isinstance(data["objectives"], list)
    assert len(data["objectives"]) >= 2
    first_obj = data["objectives"][0]
    assert "title" in first_obj
    assert "key_results" in first_obj


def test_chat():
    payload = {
        "message": "How are we doing on our Q3 goals?",
        "metrics": {"wau": 1200, "nps": 42},
        "persona": "checker",
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert data["reply"].lower().startswith("performance check:")