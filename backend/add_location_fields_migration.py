"""
Migration script to add country and city fields to users table
Run this script to update existing database schema
"""

from sqlalchemy import create_engine, text
from app.database import SQLALCHEMY_DATABASE_URL
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_location_fields():
    """Add country and city fields to users table"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    try:
        with engine.connect() as connection:
            # Check if columns already exist
            check_country = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='country'
            """)
            
            check_city = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='city'
            """)
            
            country_exists = connection.execute(check_country).fetchone()
            city_exists = connection.execute(check_city).fetchone()
            
            # Add country column if it doesn't exist
            if not country_exists:
                alter_country = text("""
                    ALTER TABLE users 
                    ADD COLUMN country VARCHAR(3)
                """)
                connection.execute(alter_country)
                logger.info("Added 'country' column to users table")
            else:
                logger.info("Column 'country' already exists in users table")
            
            # Add city column if it doesn't exist
            if not city_exists:
                alter_city = text("""
                    ALTER TABLE users 
                    ADD COLUMN city VARCHAR(100)
                """)
                connection.execute(alter_city)
                logger.info("Added 'city' column to users table")
            else:
                logger.info("Column 'city' already exists in users table")
            
            # Commit the changes
            connection.commit()
            logger.info("Migration completed successfully")
            
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise e

if __name__ == "__main__":
    add_location_fields() 