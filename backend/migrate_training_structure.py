#!/usr/bin/env python3
"""
Migration script to update Training table structure from old format to new JSON format
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any
import uuid

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import get_db, engine
from app.models.database_models import Training


def migrate_old_training_to_new():
    """
    Migrate existing training records from old structure to new structure
    """
    print("Starting migration of training records...")
    
    # Create a session
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # First, let's see if we have the old structure columns
        result = db.execute(text("PRAGMA table_info(trainings)"))
        columns = [row[1] for row in result.fetchall()]
        
        print(f"Current columns: {columns}")
        
        # Check if we have old structure columns
        has_old_structure = any(col in columns for col in ['header_badges', 'course_info', 'coach_data'])
        
        if not has_old_structure:
            print("Database already appears to be in new format or empty. Skipping migration.")
            return
        
        # Get all existing training records
        old_trainings = db.execute(text("SELECT * FROM trainings")).fetchall()
        
        print(f"Found {len(old_trainings)} training records to migrate")
        
        # Create new table structure
        print("Creating new training table structure...")
        
        # Drop the existing table and recreate with new structure
        db.execute(text("DROP TABLE IF EXISTS trainings_backup"))
        db.execute(text("CREATE TABLE trainings_backup AS SELECT * FROM trainings"))
        
        # Drop and recreate the trainings table
        db.execute(text("DROP TABLE trainings"))
        
        # Create new table with new structure
        create_new_table_sql = """
        CREATE TABLE trainings (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            activity_type VARCHAR(100) NOT NULL,
            program_goal JSON NOT NULL,
            training_environment JSON NOT NULL,
            difficulty_level VARCHAR(50) NOT NULL,
            course_duration_weeks INTEGER NOT NULL,
            weekly_training_frequency VARCHAR(50) NOT NULL,
            average_workout_duration VARCHAR(50) NOT NULL,
            age_group JSON NOT NULL,
            gender_orientation VARCHAR(50) NOT NULL,
            physical_limitations JSON,
            required_equipment JSON NOT NULL,
            course_language VARCHAR(50) NOT NULL,
            visual_content JSON NOT NULL,
            trainer_feedback_options JSON NOT NULL,
            tags JSON,
            average_course_rating FLOAT DEFAULT 0.0,
            active_participants INTEGER DEFAULT 0,
            number_of_reviews INTEGER DEFAULT 0,
            certification JSON NOT NULL,
            experience JSON NOT NULL,
            trainer_name VARCHAR(100) NOT NULL,
            course_title VARCHAR(255) NOT NULL,
            program_description TEXT NOT NULL,
            training_plan JSON NOT NULL,
            course_id VARCHAR(255) NOT NULL UNIQUE,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
        
        db.execute(text(create_new_table_sql))
        
        print("Migrating training records...")
        
        # Migrate each old training record
        for old_training in old_trainings:
            try:
                # Parse old JSON fields
                header_badges = json.loads(old_training[2]) if old_training[2] else {}
                course_info = json.loads(old_training[3]) if old_training[3] else {}
                training_plan = json.loads(old_training[4]) if old_training[4] else []
                coach_data = json.loads(old_training[5]) if old_training[5] else {}
                training_metadata = json.loads(old_training[6]) if old_training[6] else {}
                
                # Map old structure to new structure
                new_training_data = {
                    'id': old_training[0],
                    'user_id': old_training[1],
                    'activity_type': extract_activity_type(header_badges, course_info),
                    'program_goal': extract_program_goal(training_metadata, course_info),
                    'training_environment': extract_training_environment(header_badges),
                    'difficulty_level': extract_difficulty_level(header_badges, course_info),
                    'course_duration_weeks': extract_course_duration(training_plan),
                    'weekly_training_frequency': extract_frequency(training_metadata),
                    'average_workout_duration': extract_duration(training_plan),
                    'age_group': extract_age_group(training_metadata),
                    'gender_orientation': extract_gender_orientation(training_metadata),
                    'physical_limitations': extract_physical_limitations(training_metadata),
                    'required_equipment': extract_equipment(header_badges),
                    'course_language': extract_language(course_info),
                    'visual_content': extract_visual_content(training_metadata),
                    'trainer_feedback_options': extract_feedback_options(training_metadata),
                    'tags': extract_tags(training_metadata, header_badges),
                    'average_course_rating': course_info.get('rating', 0.0),
                    'active_participants': 0,  # Reset for new system
                    'number_of_reviews': course_info.get('reviews', 0),
                    'certification': extract_certification(coach_data),
                    'experience': extract_experience(coach_data),
                    'trainer_name': coach_data.get('name', course_info.get('author', 'Unknown')),
                    'course_title': course_info.get('title', 'Untitled Course'),
                    'program_description': course_info.get('description', ''),
                    'training_plan': training_plan,
                    'course_id': course_info.get('id', str(uuid.uuid4())),
                    'is_active': old_training[7],  # is_active
                    'created_at': old_training[8],  # created_at
                    'updated_at': old_training[9]   # updated_at
                }
                
                # Insert the migrated data
                insert_sql = """
                INSERT INTO trainings (
                    id, user_id, activity_type, program_goal, training_environment,
                    difficulty_level, course_duration_weeks, weekly_training_frequency,
                    average_workout_duration, age_group, gender_orientation,
                    physical_limitations, required_equipment, course_language,
                    visual_content, trainer_feedback_options, tags,
                    average_course_rating, active_participants, number_of_reviews,
                    certification, experience, trainer_name, course_title,
                    program_description, training_plan, course_id, is_active,
                    created_at, updated_at
                ) VALUES (
                    :id, :user_id, :activity_type, :program_goal, :training_environment,
                    :difficulty_level, :course_duration_weeks, :weekly_training_frequency,
                    :average_workout_duration, :age_group, :gender_orientation,
                    :physical_limitations, :required_equipment, :course_language,
                    :visual_content, :trainer_feedback_options, :tags,
                    :average_course_rating, :active_participants, :number_of_reviews,
                    :certification, :experience, :trainer_name, :course_title,
                    :program_description, :training_plan, :course_id, :is_active,
                    :created_at, :updated_at
                )
                """
                
                # Convert lists and dicts to JSON strings for SQLite
                for key in ['program_goal', 'training_environment', 'age_group', 'physical_limitations', 
                           'required_equipment', 'visual_content', 'trainer_feedback_options', 'tags',
                           'certification', 'experience', 'training_plan']:
                    new_training_data[key] = json.dumps(new_training_data[key])
                
                db.execute(text(insert_sql), new_training_data)
                
                print(f"Migrated training ID {old_training[0]}")
                
            except Exception as e:
                print(f"Error migrating training ID {old_training[0]}: {e}")
                continue
        
        db.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def extract_activity_type(header_badges, course_info):
    """Extract activity type from old data"""
    badges = header_badges.get('training_type', [])
    if badges:
        return badges[0].get('text', 'General Fitness')
    return 'General Fitness'


def extract_program_goal(metadata, course_info):
    """Extract program goals from old data"""
    return ['General Fitness']  # Default value


def extract_training_environment(header_badges):
    """Extract training environment from header badges"""
    return ['Universal']  # Default value


def extract_difficulty_level(header_badges, course_info):
    """Extract difficulty level"""
    badges = header_badges.get('training_info', [])
    for badge in badges:
        text = badge.get('text', '').lower()
        if 'beginner' in text:
            return 'Beginner'
        elif 'intermediate' in text:
            return 'Intermediate'
        elif 'advanced' in text:
            return 'Advanced'
    return 'Beginner'


def extract_course_duration(training_plan):
    """Extract course duration from training plan"""
    if training_plan:
        return len(training_plan)  # Number of training days
    return 1


def extract_frequency(metadata):
    """Extract training frequency"""
    return '3-4 times'  # Default value


def extract_duration(training_plan):
    """Extract workout duration"""
    return '30-45 minutes'  # Default value


def extract_age_group(metadata):
    """Extract age group"""
    return ['All Ages']  # Default value


def extract_gender_orientation(metadata):
    """Extract gender orientation"""
    return 'Universal'  # Default value


def extract_physical_limitations(metadata):
    """Extract physical limitations"""
    return []  # Default empty


def extract_equipment(header_badges):
    """Extract required equipment"""
    badges = header_badges.get('training_equipment', [])
    if badges:
        return [badge.get('text', 'No Equipment') for badge in badges]
    return ['No Equipment']


def extract_language(course_info):
    """Extract course language"""
    return 'English'  # Default value


def extract_visual_content(metadata):
    """Extract visual content"""
    return ['Text Instructions']  # Default value


def extract_feedback_options(metadata):
    """Extract trainer feedback options"""
    return ['Self-Guided']  # Default value


def extract_tags(metadata, header_badges):
    """Extract tags from metadata"""
    tags = metadata.get('tags', {})
    if isinstance(tags, dict):
        return list(tags.keys())
    return []


def extract_certification(coach_data):
    """Extract certification from coach data"""
    return {
        'Type': 'General',
        'Level': 'Basic',
        'Specialization': 'Fitness'
    }


def extract_experience(coach_data):
    """Extract experience from coach data"""
    return {
        'Years': coach_data.get('years', 1),
        'Specialization': 'Fitness',
        'Courses': 1,
        'Rating': coach_data.get('rating', 5.0)
    }


if __name__ == "__main__":
    migrate_old_training_to_new() 