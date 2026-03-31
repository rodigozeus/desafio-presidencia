"""Seed script to create initial admin user and sample orders."""
import httpx
import time

USERS_URL = "http://localhost:8001"
ORDERS_URL = "http://localhost:8002"

def wait_for_service(url, name, retries=10):
    for i in range(retries):
        try:
            r = httpx.get(f"{url}/health", timeout=2)
            if r.status_code == 200:
                print(f"✓ {name} is up")
                return True
        except Exception:
            pass
        print(f"  Waiting for {name}... ({i+1}/{retries})")
        time.sleep(2)
    return False

def seed():
    if not wait_for_service(USERS_URL, "Users Service"):
        print("✗ Users service not available")
        return

    if not wait_for_service(ORDERS_URL, "Orders Service"):
        print("✗ Orders service not available")
        return

    # Create admin user
    r = httpx.post(f"{USERS_URL}/users/", json={
        "name": "Administrador",
        "email": "admin@demo.com",
        "password": "admin123",
        "role": "admin"
    })
    if r.status_code == 201:
        print("✓ Admin user created: admin@demo.com / admin123")
    elif r.status_code == 400:
        print("  Admin user already exists")

    # Create operator user
    r = httpx.post(f"{USERS_URL}/users/", json={
        "name": "Operador Demo",
        "email": "operador@demo.com",
        "password": "operador123",
        "role": "operator"
    })
    if r.status_code == 201:
        print("✓ Operator user created: operador@demo.com / operador123")

    # Login as admin
    r = httpx.post(f"{USERS_URL}/auth/login", json={
        "email": "admin@demo.com",
        "password": "admin123"
    })
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create sample orders
    sample_orders = [
        {
            "customer_name": "João da Silva",
            "customer_email": "joao@cliente.com",
            "items": [
                {"product_name": "Notebook Dell Inspiron", "quantity": 1, "unit_price": 3500.00},
                {"product_name": "Mouse sem fio", "quantity": 1, "unit_price": 89.90}
            ],
            "notes": "Entrega urgente para escritório"
        },
        {
            "customer_name": "Maria Fernanda",
            "customer_email": "maria@cliente.com",
            "items": [
                {"product_name": "Smartphone Samsung", "quantity": 2, "unit_price": 1200.00}
            ],
            "notes": None
        },
        {
            "customer_name": "Carlos Eduardo",
            "customer_email": "carlos@cliente.com",
            "items": [
                {"product_name": "Teclado mecânico", "quantity": 1, "unit_price": 350.00},
                {"product_name": "Monitor 24\"", "quantity": 1, "unit_price": 850.00},
                {"product_name": "Webcam HD", "quantity": 1, "unit_price": 220.00}
            ],
            "notes": "Presente de aniversário"
        },
    ]

    for order_data in sample_orders:
        r = httpx.post(f"{ORDERS_URL}/orders/", json=order_data, headers=headers)
        if r.status_code == 201:
            print(f"✓ Order created for {order_data['customer_name']}")

    print("\n🚀 Seed complete! Access the app at http://localhost:3000")
    print("   Login: admin@demo.com / admin123")

if __name__ == "__main__":
    seed()
