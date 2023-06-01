import json


def test_create_user(client):
    data = {"name": "test", "surname": "user", "email": "testuser@nofoobar.com", "password": "testing"}
    response = client.post("/users/", json=data)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True
