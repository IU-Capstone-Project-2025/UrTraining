#!/usr/bin/env python3
"""
Migration script to add training_progress table
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
    """Add training_progress table to the database"""
    
    print("Starting migration: Adding training_progress table...")
    
    # Create the training_progress table
    try:
        # SQL to create the training_progress table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS training_progress (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id),
            training_id INTEGER NOT NULL REFERENCES trainings(id),
            completed_items JSONB DEFAULT '[]'::jsonb,
            total_items INTEGER DEFAULT 0,
            progress_percentage REAL DEFAULT 0.0,
            last_completed_item INTEGER,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT unique_user_training_progress UNIQUE (user_id, training_id)
        );
        """
        
        # Create indexes for better performance
        create_indexes_sql = """
        CREATE INDEX IF NOT EXISTS idx_training_progress_user_id ON training_progress(user_id);
        CREATE INDEX IF NOT EXISTS idx_training_progress_training_id ON training_progress(training_id);
        CREATE INDEX IF NOT EXISTS idx_training_progress_percentage ON training_progress(progress_percentage);
        """
        
        with engine.connect() as connection:
            connection.execute(text(create_table_sql))
            connection.execute(text(create_indexes_sql))
            connection.commit()
            
        print("✅ Successfully created training_progress table")
        
    except Exception as e:
        print(f"❌ Error creating training_progress table: {e}")
        return False
    
    return True

def rollback_migration():
    """Remove training_progress table (rollback)"""
    
    print("Rolling back migration: Removing training_progress table...")
    
    try:
        drop_table_sql = "DROP TABLE IF EXISTS training_progress CASCADE;"
        
        with engine.connect() as connection:
            connection.execute(text(drop_table_sql))
            connection.commit()
            
        print("✅ Successfully removed training_progress table")
        
    except Exception as e:
        print(f"❌ Error removing training_progress table: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_migration()
    else:
        success = run_migration()
    
    sys.exit(0 if success else 1) 