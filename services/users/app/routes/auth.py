from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import LoginRequest, TokenResponse, UserResponse
from ..auth import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    token = create_access_token({"sub": str(user.id), "email": user.email, "role": user.role})
    return TokenResponse(
        access_token=token,
        user=UserResponse.model_validate(user)
    )
