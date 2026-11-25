import os
from dotenv import load_dotenv

# load data from env file
load_dotenv()

class Settings:
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # Free Multimodal (Vision) models on OpenRouter with automatic fallback
    FREE_VISION_MODELS: list[str] = [
        "google/gemini-2.0-flash-exp:free",
        "qwen/qwen2.5-vl-72b-instruct:free",
        "meta-llama/llama-3.2-11b-vision-instruct:free",
        # add glm and deepseek 
    ]

settings = Settings()