import openai
from langdetect import detect
from src.logger import get_logger

logger = get_logger("translation")

def detect_language(text: str) -> str:
    try:
        lang = detect(text)
        logger.info(f"Detected language: {lang} for text: {text}")
        return lang
    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "en"

def translate(text: str, target_lang: str) -> str:
    prompt = f"Translate to {target_lang}: \"{text}\""
    logger.info(f"Translating to {target_lang}: {text}")
    resp = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role":"system","content": prompt}]
    )
    result = resp.choices[0].message.content
    logger.info(f"Translation result: {result}")
    return result
