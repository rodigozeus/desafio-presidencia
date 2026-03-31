import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import orders

logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "service": "orders", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Orders Service",
    description="Serviço de gerenciamento de pedidos com sugestão de prioridade via IA",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(orders.router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "orders"}

@app.on_event("startup")
def startup_event():
    logger.info("Orders service started")
