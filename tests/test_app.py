import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test GET /activities

def test_get_activities():
    # Arrange: (No setup needed for initial state)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data  # Should not be empty

# Test POST /activities/{activity}/signup

def test_signup_participant():
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser1@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Confirm participant is in the list
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

# Test duplicate signup

def test_signup_duplicate():
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()

# Test DELETE /activities/{activity}/signup

def test_delete_participant():
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser3@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Confirm participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]

# Test deleting non-existent participant

def test_delete_nonexistent_participant():
    # Arrange
    activity = next(iter(client.get("/activities").json().keys()))
    email = "notregistered@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()
