
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator
from app.config.setting import get_settings

# Load settings
settings = get_settings()

# Configure logging
logging.basicConfig(level=logging.INFO)

print("settings.DATABASE_URI",settings.DATABASE_URI)
# Create database engine
engine = create_engine(
    settings.DATABASE_URI,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=0
)

# Create database engine
engine_p2024 = create_engine(
    settings.DATABASE_URI_P2024,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=0
)

# Create database engine
engine_bronze = create_engine(
    settings.DATABASE_URI_BRONZE,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=20,
    max_overflow=0
)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create session factory
SessionLocalP2024 = sessionmaker(bind=engine_p2024, autocommit=False, autoflush=False)

# Create session factory
SessionLocalBronze = sessionmaker(bind=engine_bronze, autocommit=False, autoflush=False)


# Declare Base for models
Base = declarative_base()

# Dependency for session management
def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_session_p2024() -> Generator:
    sessionp2024 = SessionLocalP2024()
    try:
        yield sessionp2024
    finally:
        sessionp2024.close()


def get_session_bronze() -> Generator:
    sessionbroze = SessionLocalBronze()
    try:
        yield sessionbroze
    finally:
        sessionbroze.close()
