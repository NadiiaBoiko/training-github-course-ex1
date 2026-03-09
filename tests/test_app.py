def test_signup_nonexistent_activity():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_signup_twice_for_same_activity():
    # Arrange
    test_email = "testuser2@mergington.edu"
    activity = "Chess Club"

    # Act
    first_response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    second_response = client.post(f"/activities/{activity}/signup", params={"email": test_email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"

    # Cleanup
    client.post(f"/activities/{activity}/unregister", params={"email": test_email})

def test_unregister_nonexistent_activity():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_not_registered_email():
    # Arrange
    test_email = "notregistered@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student not registered for this activity"
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange
    # (No setup needed for in-memory activities)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"

    # Act
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": test_email})
    # Assert
    assert signup_response.status_code == 200
    assert f"Signed up {test_email}" in signup_response.json()["message"]

    # Act
    unregister_response = client.post(f"/activities/{activity}/unregister", params={"email": test_email})
    # Assert
    assert unregister_response.status_code == 200
    assert f"Removed {test_email}" in unregister_response.json()["message"]
