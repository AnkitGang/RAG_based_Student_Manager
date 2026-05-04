import logging
import requests

logger = logging.getLogger(__name__)
OLLAMA_URL = "http://localhost:11434/api/generate"


def ask_llm(prompt: str) -> str:
    try:
        res = requests.post(
            OLLAMA_URL,
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        res.raise_for_status()

        data = res.json()
        return data.get("response", "")

    except requests.exceptions.RequestException as e:
        logger.error(f"Exception occurred {e}")
        return "Unexpected error occurred"
