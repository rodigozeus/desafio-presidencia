def test_login_success(client):
    client.post("/users/", json={
        "name": "Admin",
        "email": "admin@example.com",
        "password": "senha123",
        "role": "admin"
    })
    response = client.post("/auth/login", json={
        "email": "admin@example.com",
        "password": "senha123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"]["email"] == "admin@example.com"

def test_login_wrong_password(client):
    client.post("/users/", json={
        "name": "A",
        "email": "a@example.com",
        "password": "correct",
        "role": "operator"
    })
    response = client.post("/auth/login", json={
        "email": "a@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401

def test_login_nonexistent_user(client):
    response = client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "senha"
    })
    assert response.status_code == 401
