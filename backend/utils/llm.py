import os
import logging
from dotenv import load_dotenv

# Load environment variables first
env_path = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

# We set OPENAI_API_BASE so LangChain/OpenAI client will call Groq endpoint
MOONSHOT_BASE = os.getenv("MOONSHOT_BASE_URL")
if MOONSHOT_BASE:
    os.environ["OPENAI_API_BASE"] = MOONSHOT_BASE  # LangChain/OpenAI will use this

# set API key for OpenAI client
MOONSHOT_KEY = os.getenv("MOONSHOT_API_KEY")
if MOONSHOT_KEY:
    os.environ["OPENAI_API_KEY"] = MOONSHOT_KEY

from langchain_openai import ChatOpenAI

def get_chat_llm(model_name: str = None, temperature: float = 0.0):
    """
    Returns a ChatOpenAI model configured to use MOONSHOT endpoint - REQUIRED for agentic operation
    """
    # Check if API key is available - FAIL FAST if not available
    moonshot_key = os.getenv("MOONSHOT_API_KEY")
    if not moonshot_key:
        raise ValueError("❌ MOONSHOT_API_KEY is REQUIRED for agentic operation - No fallbacks allowed")
    
    # Ensure env vars are set for OpenAI-compatible endpoint
    os.environ["OPENAI_API_KEY"] = moonshot_key
    
    moonshot_base = os.getenv("MOONSHOT_BASE_URL")
    if moonshot_base:
        os.environ["OPENAI_API_BASE"] = moonshot_base
    
    model = model_name or os.getenv("MOONSHOT_MODEL") or "llama-3.1-70b-versatile"
    try:
        llm = ChatOpenAI(
            model=model, 
            temperature=temperature,
            openai_api_key=moonshot_key,
            openai_api_base=moonshot_base
        )
        logging.info(f"✅ MOONSHOT LLM initialized successfully with model: {model}")
        return llm
    except Exception as e:
        logging.error(f"❌ Failed to initialize MOONSHOT LLM: {e}")
        raise ValueError(f"MOONSHOT LLM initialization failed - Agentic operation impossible: {e}")
