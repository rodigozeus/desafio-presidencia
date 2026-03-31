import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_TEST_URL = "sqlite:///./test_orders.db"
engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    with patch("app.routes.orders.cache_get", return_value=None), \
         patch("app.routes.orders.cache_set"), \
         patch("app.routes.orders.cache_delete_pattern"), \
         patch("app.ai_service.suggest_priority_and_summary", return_value={"priority": "medium", "summary": "Test summary"}):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()

ORDER_PAYLOAD = {
    "customer_name": "Maria Souza",
    "customer_email": "maria@example.com",
    "items": [
        {"product_name": "Notebook", "quantity": 1, "unit_price": 3500.00}
    ],
    "notes": "Entrega urgente"
}
