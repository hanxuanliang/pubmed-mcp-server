from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings.
    
    Attributes:
        pdf_output_path: Directory path where PDF files will be stored
    """
    download_path: str = "/tmp/pubmed-pdfs"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
