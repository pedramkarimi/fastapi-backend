from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from pathlib import Path


APP_ENV = os.getenv("APP_ENV", "dev")
BASE_DIR = Path(__file__).resolve().parents[2]  
ENV_FILE = BASE_DIR / f".env.{APP_ENV}"

if not ENV_FILE.exists():
    raise RuntimeError(f"Env file not found: {ENV_FILE}")



class Settings(BaseSettings):
    DEBUG: bool = False

    # POSGRESQL 
    DB_HOST: str 
    DB_PORT: int 
    DB_NAME: str 
    DB_USER: str 
    DB_PASSWORD: str 

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    # JWT
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str 
    JWT_ACCESS_TOKEN_EXPIRE_HOURS: int 

    # REDIS
    REDIS_HOST: str 
    REDIS_PORT: int 
    REDIS_DB: int 

    @property
    def REDIS_URL(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    # REDIS KEY CONFIG
    LOGIN_MAX_ATTEMPTS_PER_EMAIL: int 
    LOGIN_MAX_ATTEMPTS_PER_IP: int
    LOGIN_ATTEMPT_WINDOW_SECONDS: int 
    LOGIN_LOCK_TTL_SECONDS: int 
    RATELIMIT_DEFAULT_MAX_REQUESTS: int 
    RATELIMIT_DEFAULT_WINDOW_SECONDS: int
    CACHED_DATA_TTL: int


    # RABBITMQ
    RABBITMQ_HOST: str 
    RABBITMQ_PORT: int 
    RABBITMQ_USER: str 
    RABBITMQ_PASSWORD: str 
    WELCOME_EMAIL_QUEUE: str


    # CORS
    BACKEND_CORS_ORIGINS : list[str]
    

    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE)
    )

settings = Settings()
