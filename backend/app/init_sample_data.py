"""
Module to initialize sample data in the database
"""

from app.database import SessionLocal
from app.crud import get_user_by_username, create_user, update_training_profile, create_training
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
        
        # Create sample training programs
        sample_trainings = [
            {
                "metainfo": "Программа тренировок для начинающих - силовая тренировка с акцентом на основные группы мышц",
                "training_data": {
                    "monday": [
                        {
                            "exercise_name": "Pull ups",
                            "repetitions": "10",
                            "sets": "3",
                            "rest_time": "60 секунд",
                            "notes": "Если сложно - используйте резинку или гравитрон"
                        },
                        {
                            "exercise_name": "Push ups",
                            "repetitions": "15",
                            "sets": "3",
                            "rest_time": "45 секунд"
                        },
                        {
                            "exercise_name": "Squats",
                            "repetitions": "20",
                            "sets": "3",
                            "rest_time": "60 секунд"
                        }
                    ],
                    "wednesday": [
                        {
                            "exercise_name": "Plank",
                            "duration": "1:00",
                            "sets": "3",
                            "rest_time": "30 секунд"
                        },
                        {
                            "exercise_name": "Crunches",
                            "repetitions": "34",
                            "sets": "3",
                            "rest_time": "30 секунд"
                        }
                    ],
                    "friday": [
                        {
                            "exercise_name": "Deadlift",
                            "repetitions": "8",
                            "sets": "4",
                            "weight": "60",
                            "rest_time": "2 минуты",
                            "notes": "Следите за техникой выполнения"
                        },
                        {
                            "exercise_name": "Bench Press",
                            "repetitions": "10",
                            "sets": "3",
                            "weight": "40",
                            "rest_time": "90 секунд"
                        }
                    ]
                },
                "title": "Программа для начинающих",
                "description": "Комплексная программа тренировок на неделю для людей с начальным уровнем подготовки",
                "duration_weeks": 4,
                "difficulty_level": "beginner",
                "created_by": "admin"
            },
            {
                "metainfo": "Интенсивная кардио программа для сжигания жира и улучшения выносливости",
                "training_data": {
                    "monday": [
                        {
                            "exercise_name": "Running",
                            "duration": "30:00",
                            "notes": "Средний темп, контролируйте пульс"
                        },
                        {
                            "exercise_name": "Burpees",
                            "repetitions": "15",
                            "sets": "4",
                            "rest_time": "45 секунд"
                        }
                    ],
                    "tuesday": [
                        {
                            "exercise_name": "Jumping Jacks",
                            "duration": "2:00",
                            "sets": "5",
                            "rest_time": "30 секунд"
                        },
                        {
                            "exercise_name": "Mountain Climbers",
                            "duration": "1:30",
                            "sets": "4",
                            "rest_time": "45 секунд"
                        }
                    ],
                    "thursday": [
                        {
                            "exercise_name": "Cycling",
                            "duration": "45:00",
                            "notes": "Интервальная тренировка - 2 мин быстро, 1 мин медленно"
                        }
                    ],
                    "saturday": [
                        {
                            "exercise_name": "HIIT Circuit",
                            "duration": "25:00",
                            "notes": "Круговая тренировка: берпи, приседания, отжимания, планка"
                        }
                    ]
                },
                "title": "Кардио жиросжигание",
                "description": "Интенсивная программа для быстрого сжигания жира и развития выносливости",
                "duration_weeks": 6,
                "difficulty_level": "intermediate",
                "created_by": "admin"
            },
            {
                "metainfo": "Домашняя тренировка без оборудования для поддержания формы",
                "training_data": {
                    "monday": [
                        {
                            "exercise_name": "Push ups",
                            "repetitions": "12",
                            "sets": "3",
                            "rest_time": "45 секунд"
                        },
                        {
                            "exercise_name": "Squats",
                            "repetitions": "20",
                            "sets": "3",
                            "rest_time": "45 секунд"
                        },
                        {
                            "exercise_name": "Plank",
                            "duration": "45 секунд",
                            "sets": "3",
                            "rest_time": "30 секунд"
                        }
                    ],
                    "wednesday": [
                        {
                            "exercise_name": "Lunges",
                            "repetitions": "12 на каждую ногу",
                            "sets": "3",
                            "rest_time": "45 секунд"
                        },
                        {
                            "exercise_name": "Pike Push ups",
                            "repetitions": "8",
                            "sets": "3",
                            "rest_time": "60 секунд"
                        }
                    ],
                    "friday": [
                        {
                            "exercise_name": "Glute Bridges",
                            "repetitions": "15",
                            "sets": "3",
                            "rest_time": "30 секунд"
                        },
                        {
                            "exercise_name": "Wall Sit",
                            "duration": "30 секунд",
                            "sets": "3",
                            "rest_time": "60 секунд"
                        }
                    ],
                    "sunday": [
                        {
                            "exercise_name": "Yoga Flow",
                            "duration": "20:00",
                            "notes": "Легкая растяжка и релаксация"
                        }
                    ]
                },
                "title": "Домашняя тренировка",
                "description": "Эффективная программа для тренировок дома без специального оборудования",
                "duration_weeks": 8,
                "difficulty_level": "beginner",
                "created_by": "user"
            }
        ]
        
        # Create training programs
        for training_data in sample_trainings:
            create_training(db, training_data, admin_user.id)
        
        logger.info("Sample data initialized successfully!")
        
    except Exception as e:
        logger.error(f"Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close() 