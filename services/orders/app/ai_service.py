import logging
from typing import Optional
from .config import settings

logger = logging.getLogger(__name__)

def suggest_priority_and_summary(customer_name: str, items: list, notes: Optional[str] = None) -> dict:
    """Use Claude API to suggest order priority and generate a summary."""
    if not settings.ANTHROPIC_API_KEY:
        return {"priority": "medium", "summary": None}

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

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

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        import json
        result = json.loads(message.content[0].text.strip())
        priority = result.get("priority", "medium")
        if priority not in ("low", "medium", "high"):
            priority = "medium"
        return {"priority": priority, "summary": result.get("summary")}

    except Exception as e:
        logger.warning(f"AI service error: {e}")
        return {"priority": "medium", "summary": None}
