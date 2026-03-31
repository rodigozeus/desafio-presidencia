import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Enum as SAEnum, Float, JSON, Integer, Sequence
from sqlalchemy.dialects.postgresql import UUID
from .database import Base

order_number_seq = Sequence("order_number_seq")

class OrderStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderPriority(str, enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_number = Column(Integer, order_number_seq, nullable=False, unique=True, index=True)
    customer_name = Column(String(255), nullable=False)
    customer_email = Column(String(255), nullable=False, index=True)
    items = Column(JSON, nullable=False, default=list)
    total_amount = Column(Float, nullable=False, default=0.0)
    status = Column(SAEnum(OrderStatus), default=OrderStatus.pending, nullable=False, index=True)
    priority = Column(SAEnum(OrderPriority), default=OrderPriority.medium, nullable=False)
    notes = Column(String(1000), nullable=True)
    ai_summary = Column(String(2000), nullable=True)
    created_by = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
