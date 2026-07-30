import logging

import httpx

from app.config import settings

logger = logging.getLogger(__name__)


def ollama_chat(system_prompt: str, user_prompt: str, timeout: int = 300) -> str:
    try:
        resp = httpx.post(
            f"{settings.ollama_base_url}/api/chat",
            json={
                "model": settings.ollama_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
            },
            timeout=timeout,
        )
        resp.raise_for_status()
        return resp.json()["message"]["content"]
    except httpx.RequestError as e:
        logger.error("Ollama request failed: %s", e)
        return f"ERROR: LLM service unavailable — {e}"
