import os, openai
from tenacity import retry, wait_exponential, stop_after_attempt
from src.config import settings
from src.logger import get_logger

openai.api_key = settings.OPENAI_API_KEY
logger = get_logger("openai_agent")

@retry(wait=wait_exponential(min=1, max=10), stop=stop_after_attempt(5))
def chat_with_openai(messages: list[dict]) -> openai.ChatCompletion:
    logger.info(f"Calling OpenAI with {len(messages)} messages")
    try:
        result = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=messages
        )
        logger.info("OpenAI call successful")
        return result
    except Exception as e:
        logger.error(f"OpenAI call failed: {e}")
        raise

# If you want to use Agents SDK directly:
# agents: dict[str, Agent] = {}
# async def start_agent(chat_id: str):
#     agent = Agent(name="zoko-bot", instructions="You are a helpful assistant.")
#     agents[chat_id] = agent
