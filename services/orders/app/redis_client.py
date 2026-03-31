import redis
import json
import logging
from .config import settings

logger = logging.getLogger(__name__)

# Tenta conectar no Redis ao subir o serviço.
# Se não conseguir (container down, variável errada, qualquer coisa),
# redis_client fica None e o cache simplesmente não funciona — sem travar o sistema.
try:
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    redis_client.ping()  # ping pra confirmar que a conexão está viva de verdade
    logger.info("Redis connected")
except Exception:
    logger.warning("Redis not available, caching disabled")
    redis_client = None


def cache_get(key: str):
    # Se o Redis não está disponível, já retorna None direto — sem tentar nada
    if not redis_client:
        return None
    try:
        val = redis_client.get(key)
        # O Redis guarda tudo como string, então precisa converter de volta pra objeto Python
        return json.loads(val) if val else None
    except Exception:
        # Qualquer erro de rede/timeout: retorna None e deixa a rota buscar do banco
        return None


def cache_set(key: str, value, ttl: int = settings.CACHE_TTL):
    # Se o Redis não está disponível, ignora silenciosamente
    if not redis_client:
        return
    try:
        # setex = set + expiry: salva o valor já com o contador de TTL embutido
        # json.dumps converte o objeto Python pra string (default=str lida com datas etc.)
        redis_client.setex(key, ttl, json.dumps(value, default=str))
    except Exception:
        pass  # qualquer erro de rede/timeout: ignora e deixa o sistema seguir sem cache


# Chamado sempre que um pedido é criado ou atualizado  - apaga todas as chaves que combinam com o padrão (ex: "orders:list:*")
def cache_delete_pattern(pattern: str):
    if not redis_client:
        return
    try:
        keys = redis_client.keys(pattern)
        if keys:
            redis_client.delete(*keys)
    except Exception:
        pass
