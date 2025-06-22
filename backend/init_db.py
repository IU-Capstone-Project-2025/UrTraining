#!/usr/bin/env python3
"""
Database initialization script
Creates all tables without sample data
"""

from app.database import engine
from app.models.database_models import Base

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def main():
    """Main initialization function"""
    print("Initializing database...")
    create_tables()
    print("Database initialization completed!")

if __name__ == "__main__":
    main() 