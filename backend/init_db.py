#!/usr/bin/env python3
"""
Database initialization script
Creates all tables and adds initial sample data
"""

from app.database import engine, SessionLocal
from app.models.database_models import Base
from app.crud import create_user, update_training_profile
import json

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

def add_sample_data():
    """Add sample users and data"""
    print("Adding sample data...")
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = create_user(
            db=db,
            username="admin",
            email="admin@example.com",
            password="123",
            full_name="Administrator",
            is_admin=True
        )
        
        # Update admin training profile
        admin_profile_data = {
            "gender": "male",
            "age": 30,
            "height_cm": 180,
            "weight_kg": 75.0,
            "training_goals": ["maintain_fitness", "muscle_gain"],
            "training_level": "intermediate",
            "frequency_last_3_months": "3_4_times_week",
            "training_location": "gym",
            "location_details": "full_fitness_center",
            "session_duration": "45_60_min",
            "joint_back_problems": False,
            "chronic_conditions": False,
            "health_details": None,
            "strength_training": 4,
            "cardio": 3,
            "hiit": 3,
            "yoga_pilates": 2,
            "functional_training": 4,
            "stretching": 3
        }
        update_training_profile(db, admin_user.id, admin_profile_data)
        
        # Create regular user
        regular_user = create_user(
            db=db,
            username="user",
            email="user@example.com",
            password="password",
            full_name="Regular User",
            is_admin=False
        )
        
        # Update regular user training profile
        user_profile_data = {
            "gender": "female",
            "age": 25,
            "height_cm": 165,
            "weight_kg": 60.0,
            "training_goals": ["weight_loss", "improve_flexibility"],
            "training_level": "beginner",
            "frequency_last_3_months": "1_2_times_week",
            "training_location": "home",
            "location_details": "no_equipment",
            "session_duration": "30_45_min",
            "joint_back_problems": False,
            "chronic_conditions": False,
            "health_details": None,
            "strength_training": 2,
            "cardio": 4,
            "hiit": 2,
            "yoga_pilates": 5,
            "functional_training": 3,
            "stretching": 5
        }
        update_training_profile(db, regular_user.id, user_profile_data)
        
        print("Sample data added successfully!")
        
    except Exception as e:
        print(f"Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main initialization function"""
    print("Initializing database...")
    create_tables()
    add_sample_data()
    print("Database initialization completed!")

if __name__ == "__main__":
    main() 