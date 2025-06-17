from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://uruser:urpassword@db:5432/urtraining"
)

# Try PostgreSQL first, fallback to SQLite for local development
try:
    # Test PostgreSQL connection
    if "postgresql://" in DATABASE_URL:
        engine = create_engine(DATABASE_URL)
        # Try to connect
        conn = engine.connect()
        conn.close()
        print("Connected to PostgreSQL database")
    else:
        engine = create_engine(DATABASE_URL)
        print(f"Using database: {DATABASE_URL}")
except Exception as e:
    print(f"PostgreSQL connection failed: {e}")
    print("Falling back to SQLite for local development")
    DATABASE_URL = "sqlite:///./urtraining.db"
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 