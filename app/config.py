from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    DEBUG: bool = True
    APP_TITLE: str = "Advanced Async Task Engine"
    REDIS_URL: str = "redis://localhost:6379/0"
    MONGO_URI: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "task_audit_db"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
