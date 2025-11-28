from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "fastapi_db"
    DB_USER: str = "fastapi_user"
    DB_PASSWORD: str = "fastapi_password"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        # چون الان FastAPI بیرون Docker اجرا میشه → localhost
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"   

settings = Settings()
