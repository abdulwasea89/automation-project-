import json
from src.deps import db
from src.zoko_client import send_text
from src.logger import get_logger

logger = get_logger("broadcast")

with open("templates.json") as f:
    TEMPLATES = json.load(f)

def get_all_users() -> list[dict]:
    if db is None:
        logger.warning("GCP not available, returning empty user list")
        return []
    
    users = [{"chat_id": d.id, **d.to_dict()} for d in db.collection("sessions").stream()]
    logger.info(f"Fetched {len(users)} users for broadcast")
    return users

def broadcast_promo():
    users = get_all_users()
    if not users:
        logger.warning("No users found for broadcast")
        return
    
    for u in users:
        name, lang = u.get("name", u["chat_id"]), u.get("language", "en")
        text = TEMPLATES["promo"].get(lang, TEMPLATES["promo"]["en"]).format(name=name)
        send_text(u["chat_id"], text)
        logger.info(f"Sent promo to {u['chat_id']} in {lang}")
