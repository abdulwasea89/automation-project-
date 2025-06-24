import os, shopify
from src.config import settings
from src.logger import get_logger

logger = get_logger("shopify_client")

SHOP_KEY = settings.SHOPIFY_API_KEY
SHOP_PWD = settings.SHOPIFY_API_PASSWORD
SHOP_NAME = settings.SHOPIFY_STORE_NAME

shop_url = f"https://{SHOP_KEY}:{SHOP_PWD}@{SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)

def get_products(limit: int = 20):
    try:
        products = shopify.Product.find(limit=limit)
        logger.info(f"Fetched {len(products)} products from Shopify")
        return products
    except Exception as e:
        logger.error(f"Failed to fetch products from Shopify: {e}")
        return []
