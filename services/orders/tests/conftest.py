import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event as sa_event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from unittest.mock import patch
from app.main import app
from app.database import Base, get_db
from app.auth import get_current_user
from app.models import Order

SQLALCHEMY_TEST_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_TEST_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQLite doesn't support PostgreSQL sequences, so assign order_number via event
_order_counter = [0]

@sa_event.listens_for(Order, "before_insert")
def _assign_order_number(mapper, connection, target):
    if target.order_number is None:
        _order_counter[0] += 1
        target.order_number = _order_counter[0]

@pytest.fixture(autouse=True)
def setup_db():
    _order_counter[0] = 0
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
    def override_get_current_user():
        return {"sub": "test@example.com", "email": "test@example.com", "role": "operator"}
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    with patch("app.routes.orders.cache_get", return_value=None), \
         patch("app.routes.orders.cache_set"), \
         patch("app.routes.orders.cache_delete_pattern"), \
         patch("app.routes.orders.suggest_priority_and_summary", return_value={"priority": "medium", "summary": "Test summary"}):
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
