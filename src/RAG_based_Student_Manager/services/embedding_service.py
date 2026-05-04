import logging
import requests

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
logger = logging.getLogger(__name__)


def get_embeddings(text: str):
    try:
        res = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": "nomic-embed-text",
                "prompt": text
            }
        )

        res.raise_for_status()

        data = res.json()
        return data.get("embedding")

    except requests.exceptions.RequestException as e:
        logger.error(f"Exception occurred {e}")
        return None
