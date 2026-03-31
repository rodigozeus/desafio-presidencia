from .conftest import ORDER_PAYLOAD

def test_create_order(client):
    response = client.post("/orders/", json=ORDER_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "Maria Souza"
    assert data["total_amount"] == 3500.00
    assert data["status"] == "pending"
    assert "id" in data
    assert "order_number" in data

def test_list_orders(client):
    client.post("/orders/", json=ORDER_PAYLOAD)
    response = client.get("/orders/")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_filter_orders_by_status(client):
    client.post("/orders/", json=ORDER_PAYLOAD)
    response = client.get("/orders/?status=pending")
    assert response.status_code == 200
    assert all(o["status"] == "pending" for o in response.json())

def test_get_order_by_number(client):
    created = client.post("/orders/", json=ORDER_PAYLOAD).json()
    response = client.get(f"/orders/{created['order_number']}")
    assert response.status_code == 200
    assert response.json()["order_number"] == created["order_number"]

def test_get_order_not_found(client):
    response = client.get("/orders/999999")
    assert response.status_code == 404

def test_update_status(client):
    created = client.post("/orders/", json=ORDER_PAYLOAD).json()
    response = client.patch(f"/orders/{created['order_number']}/status", json={"status": "processing"})
    assert response.status_code == 200
    assert response.json()["status"] == "processing"

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
