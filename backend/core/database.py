# Libs
from sqlalchemy import create_engine  # SQLAlchemy
from sqlalchemy.orm import sessionmaker  # SQLAlchemy ORM

# Application
from core.settings import settings  # Core: Settings

# Engine
engine = create_engine(settings.postgres_url)

# Session
session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
