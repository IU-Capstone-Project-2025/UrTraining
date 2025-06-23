from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://uruser:urpassword@db:5432/urtraining"
)

print(f"Attempting to connect to database: {DATABASE_URL}")

# Create engine based on database type
if "postgresql://" in DATABASE_URL:
    # PostgreSQL connection with retry logic
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            engine = create_engine(DATABASE_URL)
            # Test connection
            conn = engine.connect()
            conn.close()
            print("✅ Connected to PostgreSQL database successfully")
            break
        except Exception as e:
            retry_count += 1
            print(f"❌ PostgreSQL connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count < max_retries:
                print("⏳ Retrying in 2 seconds...")
                time.sleep(2)
            else:
                print("🔄 Max retries reached, falling back to SQLite")
                DATABASE_URL = "sqlite:///./urtraining.db"
                engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
                print(f"📁 Using SQLite database: {DATABASE_URL}")
else:
    # SQLite or other database
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    print(f"📁 Using database: {DATABASE_URL}")

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