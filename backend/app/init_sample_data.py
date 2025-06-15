"""
Module to initialize sample data in the database
"""

from app.database import SessionLocal
from app.crud import get_user_by_username, create_user, update_training_profile
import logging

logger = logging.getLogger(__name__)

def init_sample_data():
    """Initialize sample data if database is empty"""
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        admin_user = get_user_by_username(db, "admin")
        if admin_user:
            logger.info("Sample data already exists")
            return
        
        logger.info("Initializing sample data...")
        
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
        
        logger.info("Sample data initialized successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close() 