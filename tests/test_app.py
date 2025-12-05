import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_for_activity():
    activity = "Chess Club"
    email = "testuser@example.com"
    # Sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()
    # Duplicate signup should fail
    response_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert response_dup.status_code == 400
    assert "detail" in response_dup.json()

def test_unregister_from_activity():
    activity = "Chess Club"
    email = "testuser@example.com"
    from src.app import activities
    # Reset participants for isolation
    activities[activity]["participants"] = []
    # Ensure participant is signed up first
    signup_response = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup_response.status_code == 200
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200
    assert "message" in response.json()
    # Unregister again should fail
    response_dup = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response_dup.status_code == 400
    assert "detail" in response_dup.json()
