import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # GCP
    PROJECT_ID: str = os.getenv("PROJECT_ID")
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    # Shopify     
    SHOPIFY_API_KEY: str = os.getenv("SHOPIFY_API_KEY")
    SHOPIFY_API_PASSWORD: str = os.getenv("SHOPIFY_API_PASSWORD")
    SHOPIFY_STORE_NAME: str = os.getenv("SHOPIFY_STORE_NAME")
    # ZOKO
    ZOKO_API_KEY: str = os.getenv("ZOKO_API_KEY")

settings = Settings()
