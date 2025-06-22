from google.cloud import firestore, storage
from src.config import settings

db = firestore.Client(project=settings.PROJECT_ID)
bucket = storage.Client(project=settings.PROJECT_ID).bucket("zoko-ai-media")