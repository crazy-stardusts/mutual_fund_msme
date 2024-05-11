from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv('.env')


class Settings(BaseSettings):
    DATABASE_HOST: str = "localhost"
    DATABASE_DB_NAME: str = "sme_mutual_fund"
    DATABASE_DB_PASS: str = "postgres"
    DATABASE_DB_USER: str = "postgres"
    DATABASE_PORT: int = 5432
    SECRET_KEY: str = "your-secret-key"

settings = Settings()
