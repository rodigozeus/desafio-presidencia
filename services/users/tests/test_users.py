def test_create_user(client):
    response = client.post("/users/", json={
        "name": "João Silva",
        "email": "joao@example.com",
        "password": "senha123",
        "role": "operator"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "joao@example.com"
    assert data["name"] == "João Silva"
    assert "id" in data

def test_create_user_duplicate_email(client):
    payload = {"name": "A", "email": "dup@example.com", "password": "123", "role": "operator"}
    client.post("/users/", json=payload)
    response = client.post("/users/", json=payload)
    assert response.status_code == 400

def test_list_users(client):
    client.post("/users/", json={"name": "A", "email": "a@example.com", "password": "123", "role": "operator"})
    client.post("/users/", json={"name": "B", "email": "b@example.com", "password": "123", "role": "admin"})
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_list_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
