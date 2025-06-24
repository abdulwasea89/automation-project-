import os, requests
from src.config import settings
from src.logger import get_logger

BASE = "https://api.zoko.io/v1"
HEADERS = {
    "Authorization": f"Bearer {settings.ZOKO_API_KEY}",
    "Content-Type": "application/json"
}

logger = get_logger("zoko_client")

def send_text(chat_id: str, text: str):
    payload = {"to": chat_id, "type": "text", "text": {"body": text}}
    try:
        r = requests.post(f"{BASE}/messages", json=payload, headers=HEADERS)
        r.raise_for_status()
        logger.info(f"Sent text to {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send text to {chat_id}: {e}")

def send_carousel(chat_id: str, carousel: dict):
    payload = {"to": chat_id, "type": "interactive", "interactive": carousel}
    try:
        r = requests.post(f"{BASE}/messages", json=payload, headers=HEADERS)
        r.raise_for_status()
        logger.info(f"Sent carousel to {chat_id}")
    except Exception as e:
        logger.error(f"Failed to send carousel to {chat_id}: {e}")
