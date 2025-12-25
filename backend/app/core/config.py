"""
Core configuration management for Mili backend.
Loads settings from environment variables.
"""
from pydantic_settings import BaseSettings
from typing import List
import json
from dotenv import load_dotenv

# Load .env file with override=True to ensure .env takes precedence over system env vars
load_dotenv(override=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Anthropic Claude Configuration
    anthropic_api_key: str
    anthropic_base_url: str = "http://www.claudecodeserver.top/api"
    anthropic_auth_token: str = ""
    llm_model: str = "claude-3-5-sonnet-20241022"

    # Database & Storage
    database_path: str = "./chroma_db"
    upload_dir: str = "./uploads"
    max_file_size: int = 10485760  # 10MB

    # CORS Configuration
    cors_origins: str = '["http://localhost:3000"]'

    # Embedding Configuration
    embedding_model: str = "all-MiniLM-L6-v2"

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from JSON string."""
        try:
            return json.loads(self.cors_origins)
        except:
            return ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
