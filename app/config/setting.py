import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):

    # App
    APP_NAME:  str = os.getenv("APP_NAME", "FastAPI")
    DEBUG: bool = bool(os.getenv("DEBUG", False))
    STORAGE_URL:  str = os.getenv("STORAGE_URL", "http://localhost:8000")
    
    # FrontEnd Application
    FRONTEND_HOST: str = os.getenv("FRONTEND_HOST", "http://localhost:3000")

    # MySql Database Config
    POSTGRESQL_HOST: str = os.getenv("POSTGRESQL_HOST", '127.0.0.1')
    POSTGRESQL_USER: str = os.getenv("POSTGRESQL_USER", 'root')
    POSTGRESQL_PASS: str = os.getenv("POSTGRESQL_PASSWORD", 'secret')
    POSTGRESQL_PORT: int = int(os.getenv("POSTGRESQL_PORT", 3306))
    POSTGRESQL_DB: str = os.getenv("POSTGRESQL_DB", 'fastapi')
    DATABASE_URI: str = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASS}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DB}"
    DATABASE_URI_P2024: str = f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASS}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/kpu"

    POSTGRESQL_BRONZE_HOST: str = os.getenv("POSTGRESQL_BRONZE_HOST", '127.0.0.1')
    POSTGRESQL_BRONZE_USER: str = os.getenv("POSTGRESQL_BRONZE_USER", 'root')
    POSTGRESQL_BRONZE_PASS: str = os.getenv("POSTGRESQL_BRONZE_PASSWORD", 'secret')
    POSTGRESQL_BRONZE_PORT: int = int(os.getenv("POSTGRESQL_BRONZE_PORT", 3306))
    POSTGRESQL_BRONZE_DB: str = os.getenv("POSTGRESQL_BRONZE_DB", 'fastapi')
    DATABASE_URI_BRONZE: str = f"postgresql://{POSTGRESQL_BRONZE_USER}:{POSTGRESQL_BRONZE_PASS}@{POSTGRESQL_BRONZE_HOST}:{POSTGRESQL_BRONZE_PORT}/{POSTGRESQL_BRONZE_DB}"


    # JWT Secret Key
    JWT_SECRET: str = os.getenv("JWT_SECRET", "649fb93ef34e4fdf4187709c84d643dd61ce730d91856418fdcf563f895ea40f")
    JWT_ALGORITHM: str = os.getenv("ACCESS_TOKEN_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
    REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

    #google api login
    # GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "<client_id>")
    # GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET", "<client_secret>")
    # GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/v1/auth/google/callback")


    # App Secret Key
    SECRET_KEY: str = os.getenv("SECRET_KEY", "8deadce9449770680910741063cd0a3fe0acb62a8978661f421bbcbb66dc41f1")
    TASK_MANAGEMENT: str = os.getenv("TASK_MANAGEMENT", "localhost")
    DEFAULT_PASSWORD: str = os.getenv("DEFAULT_PASSWORD", "Rahasia123@")

    # Beanstalk
    # BEANSTALK_HOST: str = os.getenv("BEANSTALK_HOST", "localhost")
    # BEANSTALK_PORT: int = int(os.getenv("BEANSTALK_PORT", 11300))
    # BEANSTALK_TUBE: str = os.getenv("BEANSTALK_TUBE", "oltras")
    VERSION: str = os.getenv("VERSION", "v1")

    # REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    # REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))

    # ELASTIC_HOST: str = os.getenv("ELASTIC_HOST", "localhost")
    # ELASTIC_USERNAME: str = os.getenv("ELASTIC_USERNAME", "localhost")
    # ELASTIC_PASSWORD: str = os.getenv("ELASTIC_PASSWORD", "localhost")

    # MAP_API: str = os.getenv("MAP_API", "")
    # TEMPLATE_EXCEL_POKIR: str = os.getenv("TEMPLATE_EXCEL_POKIR", "/code/public/template/pokir_template.xlsx")
    # TEMPLATE_PREVIOUS_EXCEL_POKIR: str = os.getenv("TEMPLATE_PREVIOUS_EXCEL_POKIR", "/code/public/template/pokir_previous_template_v3.xlsx")

    # CITY_ID: str = os.getenv("CITY_ID", "3314")
    # WORKSPACE: str = os.getenv("WORKSPACE", "0")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
