from src.deps import db
from google.cloud import firestore
import time
from src.logger import get_logger

logger = get_logger("gcp")

def save_message(chat_id: str, role: str, content: str):
    if db is None:
        logger.warning("GCP not available, message not saved")
        return
    
    rec = {"role": role, "content": content, "timestamp": time.time()}
    ref = db.collection("sessions").document(chat_id)
    try:
        ref.set({"messages": []}, merge=True)
        ref.update({"messages": firestore.ArrayUnion([rec])})
        logger.info(f"Saved message for {chat_id} as {role}")
    except Exception as e:
        logger.error(f"Failed to save message for {chat_id}: {e}")

def load_history(chat_id: str) -> list[dict]:
    if db is None:
        logger.warning("GCP not available, returning empty history")
        return []
    
    try:
        doc = db.collection("sessions").document(chat_id).get()
        messages = doc.to_dict().get("messages", [])
        logger.info(f"Loaded {len(messages)} messages for {chat_id}")
        return messages
    except Exception as e:
        logger.error(f"Failed to load history for {chat_id}: {e}")
        return []
