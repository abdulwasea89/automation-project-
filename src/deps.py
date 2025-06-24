import os
from google.cloud import firestore, storage
from src.config import settings
from src.logger import get_logger

logger = get_logger("deps")

# Initialize clients with error handling
try:
    if settings.PROJECT_ID:
        db = firestore.Client(project=settings.PROJECT_ID)
        bucket = storage.Client(project=settings.PROJECT_ID).bucket("zoko-ai-media")
        logger.info(f"Successfully connected to GCP project: {settings.PROJECT_ID}")
    else:
        logger.warning("PROJECT_ID not set, GCP services will not be available")
        db = None
        bucket = None
except Exception as e:
    logger.warning(f"Failed to initialize GCP clients: {e}")
    logger.info("Running in local development mode without GCP")
    db = None
    bucket = None
