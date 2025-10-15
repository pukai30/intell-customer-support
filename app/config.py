"""
Configuration management using pydantic-settings
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    
    # MongoDB Configuration
    mongodb_url: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    mongodb_db_name: str = Field(default="customer_support", env="MONGODB_DB_NAME")
    
    # Email Configuration
    email_host: str = Field(default="smtp.gmail.com", env="EMAIL_HOST")
    email_port: int = Field(default=587, env="EMAIL_PORT")
    email_user: str = Field(..., env="EMAIL_USER")
    email_password: str = Field(..., env="EMAIL_PASSWORD")
    imap_host: str = Field(default="imap.gmail.com", env="IMAP_HOST")
    imap_port: int = Field(default=993, env="IMAP_PORT")
    
    # Twilio Configuration (Optional - can be added later)
    twilio_account_sid: Optional[str] = Field(default=None, env="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, env="TWILIO_AUTH_TOKEN")
    twilio_phone_number: Optional[str] = Field(default=None, env="TWILIO_PHONE_NUMBER")
    twilio_whatsapp_number: str = Field(default="whatsapp:+14155238886", env="TWILIO_WHATSAPP_NUMBER")
    
    # Application Configuration
    app_host: str = Field(default="0.0.0.0", env="APP_HOST")
    app_port: int = Field(default=8000, env="APP_PORT")
    debug: bool = Field(default=True, env="DEBUG")
    
    # Knowledge Base Configuration
    knowledge_base_path: str = Field(default="./knowledge_base", env="KNOWLEDGE_BASE_PATH")
    embeddings_model: str = Field(default="text-embedding-3-small", env="EMBEDDINGS_MODEL")
    llm_model: str = Field(default="gpt-4-turbo-preview", env="LLM_MODEL")
    vector_store_path: str = Field(default="./vector_store", env="VECTOR_STORE_PATH")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()

