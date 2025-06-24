import openai
from src.shopify_client import get_products
from src.logger import get_logger

logger = get_logger("recommendation")

def extract_keywords(text: str) -> list[str]:
    resp = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role":"system","content":"Extract 3–5 keywords, comma separated."},
            {"role":"user","content":text}
        ]
    )
    keywords = [kw.strip() for kw in resp.choices[0].message.content.split(",") if kw.strip()]
    logger.info(f"Extracted keywords: {keywords}")
    return keywords

def recommend_by_keywords(keywords: list[str]):
    products = get_products(limit=20)
    recs = [
        p for p in products
        if any(kw.lower() in p.title.lower() or kw.lower() in [t.lower() for t in p.tags]
               for kw in keywords)
    ]
    logger.info(f"Recommended {len(recs)} products for keywords: {keywords}")
    return recs

def build_carousel(products, store_name: str) -> dict:
    elements = []
    for p in products[:5]:
        elements.append({
            "title": p.title,
            "imageUrl": p.images[0].src if p.images else "",
            "actionUrl": f"https://{store_name}.myshopify.com/products/{p.handle}",
            "subtitle": (p.body_html or "")[:80] + "…"
        })
    return {"type":"carousel", "elements": elements}
