from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime
from .models import UserRole

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.operator

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: UserRole
    created_at: datetime

    model_config = {"from_attributes": True}

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
