
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and API keys.
    Loads variables from a .env file.
    """
    
    ROBOFLOW_API_KEY: str = "YOUR_ROBOFLOW_API_KEY_HERE"
    
    OPENAI_API_KEY: str | None = None
    
    ROBOFLOW_MODEL_ID: str = "adr/6"
    ROBOFLOW_CONFIDENCE_THRESHOLD: int = 30
    ROBOFLOW_OVERLAP_THRESHOLD: int = 50

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

settings = Settings()