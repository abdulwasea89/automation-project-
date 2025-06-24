import os
from google.cloud import firestore, storage
from src.config import settings
from src.logger import get_logger

logger = get_logger("deps")

credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if credentials_path and os.path.isfile(credentials_path):
    logger.info(f"Using credentials from: {credentials_path}")
else:
    logger.warning("GOOGLE_APPLICATION_CREDENTIALS not set or file missing, using default credentials")

try:
    if settings.PROJECT_ID:
        db = firestore.Client(project=settings.PROJECT_ID)
        bucket = storage.Client(project=settings.PROJECT_ID).bucket("zoko-ai-media")
        logger.info(f"Connected to GCP project: {settings.PROJECT_ID}")
    else:
        logger.warning("PROJECT_ID not set.")
        db = None
        bucket = None
except Exception as e:
    logger.error(f"GCP client init failed: {e}")
    db = None
    bucket = None
