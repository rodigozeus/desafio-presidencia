from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from typing import Optional, List, Any
from .models import OrderStatus, OrderPriority

class OrderItem(BaseModel):
    product_name: str
    quantity: int
    unit_price: float

class OrderCreate(BaseModel):
    customer_name: str
    customer_email: EmailStr
    items: List[OrderItem]
    notes: Optional[str] = None

class OrderStatusUpdate(BaseModel):
    status: OrderStatus

class OrderResponse(BaseModel):
    id: UUID
    order_number: int
    customer_name: str
    customer_email: str
    items: List[Any]
    total_amount: float
    status: OrderStatus
    priority: OrderPriority
    notes: Optional[str]
    ai_summary: Optional[str]
    created_by: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
