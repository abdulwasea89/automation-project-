import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # GCP
    PROJECT_ID: str = os.getenv("PROJECT_ID")
    if not PROJECT_ID:
        raise ValueError("PROJECT_ID environment variable is not set")
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    # Shopify
    SHOPIFY_API_KEY: str = os.getenv("SHOPIFY_API_KEY")
    if not SHOPIFY_API_KEY:
        raise ValueError("SHOPIFY_API_KEY environment variable is not set")
    SHOPIFY_API_PASSWORD: str = os.getenv("SHOPIFY_API_PASSWORD")
    if not SHOPIFY_API_PASSWORD:
        raise ValueError("SHOPIFY_API_PASSWORD environment variable is not set")
    SHOPIFY_STORE_NAME: str = os.getenv("SHOPIFY_STORE_NAME")
    if not SHOPIFY_STORE_NAME:
        raise ValueError("SHOPIFY_STORE_NAME environment variable is not set")
    # ZOKO
    ZOKO_API_KEY: str = os.getenv("ZOKO_API_KEY")
    if not ZOKO_API_KEY:
        raise ValueError("ZOKO_API_KEY environment variable is not set")

settings = Settings()
