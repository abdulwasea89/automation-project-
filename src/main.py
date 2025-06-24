import time
from fastapi import FastAPI, Request, HTTPException, Header
from src.config import settings
from src.gcp import save_message, load_history
from src.openai_agent import chat_with_openai
from src.zoko_client import send_text, send_carousel
from src.recommendation import extract_keywords, recommend_by_keywords, build_carousel
from src.translation import detect_language, translate
from src.shopify_client import get_products
from src.broadcast import broadcast_promo
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError as FastAPIRequestValidationError
from src.logger import get_logger
import traceback
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest
from starlette.responses import Response as StarletteResponse
import os
from collections import defaultdict
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

logger = get_logger("main")

app = FastAPI(title="ZOKO-Shopify AI Middleware")

API_KEY = os.getenv("API_KEY")
RATE_LIMIT = 30  # requests
RATE_PERIOD = 60  # seconds
rate_limit_store = defaultdict(list)

class ApiKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        if request.url.path == "/":
            return await call_next(request)
        api_key = request.headers.get("x-api-key")
        if api_key != API_KEY:
            logger.warning(f"Unauthorized access attempt from {request.client.host}")
            return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "Invalid API key"})
        return await call_next(request)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        if request.url.path == "/":
            return await call_next(request)
        ip = request.client.host
        now = time.time()
        window = [t for t in rate_limit_store[ip] if now - t < RATE_PERIOD]
        window.append(now)
        rate_limit_store[ip] = window
        if len(window) > RATE_LIMIT:
            logger.warning(f"Rate limit exceeded for {ip}")
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        return await call_next(request)

app.add_middleware(RateLimitMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

@app.exception_handler(FastAPIRequestValidationError)
async def validation_exception_handler(request, exc):
    logger.warning(f"Validation error: {exc}")
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

class ZokoMessageText(BaseModel):
    body: str

class ZokoMessage(BaseModel):
    from_: str = Field(..., alias="from")
    text: ZokoMessageText

class ZokoWebhookPayload(BaseModel):
    messages: List[ZokoMessage]

class BroadcastResponse(BaseModel):
    status: str

class HealthResponse(BaseModel):
    status: str

class TestGCPResponse(BaseModel):
    message: str

@app.get("/", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    logger.info("Health check endpoint called")
    return {"status": "ok"}

@app.get("/test-gcp", response_model=TestGCPResponse)
def test_gcp():
    """Test GCP Firestore connectivity."""
    logger.info("Test GCP endpoint called")
    save_message("test-chat", "system", "ping")
    return {"message": "GCP OK"}

@app.post("/webhook/zoko", response_model=BroadcastResponse)
async def zoko_webhook(payload: ZokoWebhookPayload):
    """Webhook endpoint for ZOKO WhatsApp integration."""
    logger.info("Received webhook from ZOKO")
    try:
        msg = payload.messages[0]
        chat_id, text = msg.from_, msg.text.body
    except Exception as e:
        logger.error(f"Invalid payload: {e}", exc_info=True)
        raise HTTPException(400, "Invalid payload")

    lang = detect_language(text)
    text_en = translate(text, "en") if lang != "en" else text
    logger.info(f"Detected language: {lang}, translated text: {text_en}")

    save_message(chat_id, "user", text_en)

    if text_en.lower().startswith("recommend"):
        kws = extract_keywords(text_en)
        logger.info(f"Extracted keywords: {kws}")
        recs = recommend_by_keywords(kws)
        carousel = build_carousel(recs, settings.SHOPIFY_STORE_NAME)
        send_carousel(chat_id, carousel)
        save_message(chat_id, "assistant", "<sent carousel>")
        logger.info(f"Sent carousel to {chat_id}")
    else:
        history = load_history(chat_id)
        history.append({"role":"user","content":text_en,"timestamp": time.time()})
        try:
            resp = chat_with_openai(history)
            reply_en = resp.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI error: {e}", exc_info=True)
            raise HTTPException(502, "AI service unavailable")
        reply = translate(reply_en, lang) if lang != "en" else reply_en
        save_message(chat_id, "assistant", reply)
        send_text(chat_id, reply)
        logger.info(f"Sent reply to {chat_id}")

    return {"status": "processed"}

@app.post("/broadcast/promo", response_model=BroadcastResponse)
def trigger_broadcast():
    """Trigger a promotional broadcast to all users."""
    logger.info("Broadcast promo triggered")
    broadcast_promo()
    return {"status": "broadcast_sent"}
