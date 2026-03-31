import json
import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"

def suggest_priority_and_summary(customer_name: str, items: list, notes: Optional[str] = None) -> dict:
    """Use Ollama (local) to suggest order priority and generate a summary."""
    try:
        items_text = "\n".join([
            f"- {item.get('product_name', item.get('name', 'Produto'))}: {item.get('quantity', 1)}x R${item.get('unit_price', 0):.2f}"
            for item in items
        ])
        total = sum(item.get('quantity', 1) * item.get('unit_price', 0) for item in items)

        prompt = f"""Analise este pedido de e-commerce e retorne APENAS um JSON válido (sem markdown, sem explicação):

Cliente: {customer_name}
Itens:
{items_text}
Total: R${total:.2f}
Observações: {notes or 'Nenhuma'}

Retorne exatamente neste formato:
{{"priority": "low|medium|high", "summary": "resumo curto em português de até 100 caracteres"}}

Critérios de prioridade:
- high: total > R$500 ou pedido urgente nas observações
- low: total < R$50 e sem urgência
- medium: demais casos"""

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=30,
        )
        response.raise_for_status()

        text = response.json()["message"]["content"].strip()
        result = json.loads(text)
        priority = result.get("priority", "medium")
        if priority not in ("low", "medium", "high"):
            priority = "medium"
        return {"priority": priority, "summary": result.get("summary")}

    except Exception as e:
        logger.warning(f"AI service error: {e}")
        return {"priority": "medium", "summary": None}
