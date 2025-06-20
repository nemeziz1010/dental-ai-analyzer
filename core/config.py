# core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Manages application settings and API keys.
    Loads variables from a .env file.
    """
    # If ROBOFLOW_API_KEY is not set in the environment, it will default to this string.
    ROBOFLOW_API_KEY: str = "YOUR_ROBOFLOW_API_KEY_HERE"
    
    # We'll make the OpenAI key optional for now to support the mock report.
    OPENAI_API_KEY: str | None = None
    
    # Roboflow model details from the project brief
    ROBOFLOW_MODEL_ID: str = "adr/6"
    ROBOFLOW_CONFIDENCE_THRESHOLD: int = 30
    ROBOFLOW_OVERLAP_THRESHOLD: int = 50

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding='utf-8', extra='ignore')

# Create a single, importable instance of the settings
settings = Settings()