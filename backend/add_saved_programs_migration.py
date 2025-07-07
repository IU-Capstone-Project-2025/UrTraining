#!/usr/bin/env python3
"""
Migration script to add saved_programs table
"""

import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from app.database import SQLALCHEMY_DATABASE_URL, engine
from app.models.database_models import Base

def run_migration():
    """Add saved_programs table to the database"""
    
    print("Starting migration: Adding saved_programs table...")
    
    # Create the saved_programs table
    try:
        # SQL to create the saved_programs table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS saved_programs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            training_id INTEGER NOT NULL REFERENCES trainings(id),
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT unique_user_training UNIQUE (user_id, training_id)
        );
        """
        
        # Create index for better performance
        create_index_sql = """
        CREATE INDEX IF NOT EXISTS idx_saved_programs_user_id ON saved_programs(user_id);
        CREATE INDEX IF NOT EXISTS idx_saved_programs_training_id ON saved_programs(training_id);
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_table_sql))
            connection.execute(text(create_index_sql))
            connection.commit()
            
        print("✅ Successfully created saved_programs table")
        
    except Exception as e:
        print(f"❌ Error creating saved_programs table: {e}")
        return False
    
    return True

def rollback_migration():
    """Remove saved_programs table (rollback)"""
    
    print("Rolling back migration: Removing saved_programs table...")
    
    try:
        drop_table_sql = "DROP TABLE IF EXISTS saved_programs CASCADE;"
        
        with engine.connect() as connection:
            connection.execute(text(drop_table_sql))
            connection.commit()
            
        print("✅ Successfully removed saved_programs table")
        
    except Exception as e:
        print(f"❌ Error removing saved_programs table: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_migration()
    else:
        success = run_migration()
    
    sys.exit(0 if success else 1) 