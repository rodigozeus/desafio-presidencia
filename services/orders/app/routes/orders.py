import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Order, OrderStatus
from ..schemas import OrderCreate, OrderStatusUpdate, OrderResponse
from ..auth import get_current_user, get_optional_user
from ..redis_client import cache_get, cache_set, cache_delete_pattern
from ..ai_service import suggest_priority_and_summary

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=List[OrderResponse])
def list_orders(
    status: Optional[OrderStatus] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_optional_user)
):
    cache_key = f"orders:list:{status}:{skip}:{limit}"
    cached = cache_get(cache_key)
    if cached:
        logger.info(f"Cache hit for {cache_key}")
        return cached

    query = db.query(Order)
    if status:
        query = query.filter(Order.status == status)
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()

    result = [OrderResponse.model_validate(o).model_dump() for o in orders]
    cache_set(cache_key, result)
    return result

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_optional_user)
):
    items_list = [item.model_dump() for item in data.items]
    total = sum(item["quantity"] * item["unit_price"] for item in items_list)

    ai_result = suggest_priority_and_summary(data.customer_name, items_list, data.notes)

    order = Order(
        customer_name=data.customer_name,
        customer_email=data.customer_email,
        items=items_list,
        total_amount=total,
        notes=data.notes,
        priority=ai_result["priority"],
        ai_summary=ai_result["summary"],
        created_by=current_user.get("email") if current_user else None,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    cache_delete_pattern("orders:list:*")
    logger.info(f"Order created: {order.id} priority={order.priority}")
    return order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_optional_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    data: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    order.status = data.status
    db.commit()
    db.refresh(order)
    cache_delete_pattern("orders:list:*")
    logger.info(f"Order {order_id} status updated to {data.status}")
    return order
