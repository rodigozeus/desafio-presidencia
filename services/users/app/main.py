import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine, SessionLocal
from .models import User
from .auth import hash_password
from .routes import auth, users
import time

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "service": "users", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Users Service",
    description="Serviço de gerenciamento de usuários e autenticação JWT",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "users"}

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            admin = User(
                name="Administrador",
                email="admin@admin.com",
                password_hash=hash_password("admin123"),
                role="admin",
            )
            db.add(admin)
            db.commit()
            logger.info("Admin inicial criado: admin@admin.com")
    finally:
        db.close()
    logger.info("Users service started")
