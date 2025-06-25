#!/usr/bin/env python3
"""
Test script to validate the new Training model structure
"""

import json
import sys
import os

# Add the parent directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.training import (
    Training, 
    TrainingCreate, 
    TrainingUpdate, 
    TrainingResponse,
    Certification,
    Experience,
    Exercise,
    TrainingDay
)


def test_training_model_with_json_data():
    """Test the training model with data from the JSON file"""
    
    # Sample data matching the JSON structure
    sample_training_data = {
        "activity_type": "Yoga",
        "program_goal": ["Competition Preparation"],
        "training_environment": ["Pool"],
        "difficulty_level": "Advanced",
        "course_duration_weeks": 2,
        "weekly_training_frequency": "1-2 times",
        "average_workout_duration": "45-60 minutes",
        "age_group": ["Young Adults (18-30)"],
        "gender_orientation": "For Men",
        "physical_limitations": [],
        "required_equipment": ["No Equipment", "Pull-up/Dip Bars"],
        "course_language": "Other",
        "visual_content": ["Progress Graphs"],
        "trainer_feedback_options": ["Personal Consultations"],
        "tags": [
            "Weight Loss", "Recovery", "Minimal Equipment", "Fat Burning",
            "Anti-Stress", "Explosive Strength", "Energy", "Arms", "Better Sleep"
        ],
        "average_course_rating": 4.99,
        "active_participants": 967,
        "number_of_reviews": 456,
        "certification": {
            "Type": "ISSA",
            "Level": "Master",
            "Specialization": "Yoga"
        },
        "experience": {
            "Years": 8,
            "Specialization": "Yoga",
            "Courses": 20,
            "Rating": 4.9
        },
        "trainer_name": "Anna Smirnova",
        "course_title": "Competition Preparation with Anna Smirnova",
        "program_description": "**Competition Preparation Yoga Program**\n**Trainer: Anna Smirnova (ISSA, Master)**",
        "training_plan": [
            {
                "title": "Week 1 - Day 1 (Monday, 60 min)",
                "exercises": [
                    {
                        "exercise": "Leg swings (front and back)",
                        "repeats": "-",
                        "sets": "1",
                        "duration": "5 min",
                        "rest": "-",
                        "description": "Dynamic warm-up"
                    },
                    {
                        "exercise": "Downward-Facing Dog (Adho Mukha Svanasana)",
                        "repeats": "-",
                        "sets": "3",
                        "duration": "30 sec",
                        "rest": "30 sec",
                        "description": "Foundational strength"
                    }
                ]
            }
        ],
        "id": "c217bc40-7553-42f9-90cd-339013cfe3b5"
    }
    
    print("Testing Training model...")
    
    try:
        # Test TrainingCreate model
        print("1. Testing TrainingCreate model...")
        training_create = TrainingCreate(**sample_training_data)
        print(f"   ✓ TrainingCreate model created successfully")
        print(f"   Activity Type: {training_create.activity_type}")
        print(f"   Course Title: {training_create.course_title}")
        print(f"   Trainer: {training_create.trainer_name}")
        
        # Test Training model (full model)
        print("\n2. Testing Training model...")
        training = Training(**sample_training_data)
        print(f"   ✓ Training model created successfully")
        print(f"   Course ID: {training.id}")
        print(f"   Duration: {training.course_duration_weeks} weeks")
        print(f"   Rating: {training.average_course_rating}")
        
        # Test TrainingResponse model
        print("\n3. Testing TrainingResponse model...")
        response_data = sample_training_data.copy()
        response_data.update({
            "db_id": 1,
            "user_id": 1,
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-01T00:00:00"
        })
        training_response = TrainingResponse(**response_data)
        print(f"   ✓ TrainingResponse model created successfully")
        print(f"   DB ID: {training_response.db_id}")
        print(f"   User ID: {training_response.user_id}")
        
        # Test individual components
        print("\n4. Testing individual model components...")
        
        # Test Certification
        cert = Certification(**sample_training_data["certification"])
        print(f"   ✓ Certification: {cert.Type} {cert.Level} - {cert.Specialization}")
        
        # Test Experience
        exp = Experience(**sample_training_data["experience"])
        print(f"   ✓ Experience: {exp.Years} years, Rating: {exp.Rating}")
        
        # Test TrainingDay and Exercise
        training_day = TrainingDay(**sample_training_data["training_plan"][0])
        print(f"   ✓ Training Day: {training_day.title}")
        print(f"   ✓ Exercises: {len(training_day.exercises)} exercises")
        
        exercise = Exercise(**training_day.exercises[0])
        print(f"   ✓ Exercise: {exercise.exercise}")
        
        # Test serialization
        print("\n5. Testing JSON serialization...")
        training_json = training.model_dump_json()
        print(f"   ✓ Successfully serialized to JSON ({len(training_json)} characters)")
        
        # Test deserialization
        training_from_json = Training.model_validate_json(training_json)
        print(f"   ✓ Successfully deserialized from JSON")
        print(f"   Matches original: {training_from_json.id == training.id}")
        
        # Test field aliases
        print("\n6. Testing field aliases...")
        json_data_with_aliases = {
            "Activity Type": "Yoga",
            "Program Goal": ["Competition Preparation"],
            "Training Environment": ["Pool"],
            "Difficulty Level": "Advanced",
            "Course Duration (weeks)": 2,
            "Weekly Training Frequency": "1-2 times",
            "Average Workout Duration": "45-60 minutes",
            "Age Group": ["Young Adults (18-30)"],
            "Gender Orientation": "For Men",
            "Physical Limitations": [],
            "Required Equipment": ["No Equipment"],
            "Course Language": "Other",
            "Visual Content": ["Progress Graphs"],
            "Trainer Feedback Options": ["Personal Consultations"],
            "Tags": ["Weight Loss"],
            "Average Course Rating": 4.99,
            "Active Participants": 967,
            "Number of Reviews": 456,
            "Certification": {
                "Type": "ISSA",
                "Level": "Master",
                "Specialization": "Yoga"
            },
            "Experience": {
                "Years": 8,
                "Specialization": "Yoga",
                "Courses": 20,
                "Rating": 4.9
            },
            "Trainer Name": "Anna Smirnova",
            "Course Title": "Competition Preparation",
            "Program Description": "Test description",
            "training_plan": [],
            "id": "test-id"
        }
        
        training_with_aliases = Training(**json_data_with_aliases)
        print(f"   ✓ Field aliases work correctly")
        print(f"   Activity Type alias: {training_with_aliases.activity_type}")
        
        print("\n✅ All tests passed! The new Training model is working correctly.")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def test_with_sample_json_file():
    """Test with data from the actual JSON file"""
    
    print("\n" + "="*60)
    print("TESTING WITH ACTUAL JSON FILE DATA")
    print("="*60)
    
    # Try to load the JSON file
    try:
        json_file_path = "selected_courses_with_ids_plus_plan.json"
        if not os.path.exists(json_file_path):
            print(f"JSON file not found: {json_file_path}")
            return False
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            courses_data = json.load(f)
        
        print(f"Loaded {len(courses_data)} courses from JSON file")
        
        # Test with the first course
        if courses_data:
            first_course = courses_data[0]
            print(f"\nTesting with first course: {first_course.get('Course Title', 'Unknown')}")
            
            # Convert the JSON field names to our model field names
            model_data = {
                "activity_type": first_course.get("Activity Type", ""),
                "program_goal": first_course.get("Program Goal", []),
                "training_environment": first_course.get("Training Environment", []),
                "difficulty_level": first_course.get("Difficulty Level", ""),
                "course_duration_weeks": first_course.get("Course Duration (weeks)", 1),
                "weekly_training_frequency": first_course.get("Weekly Training Frequency", ""),
                "average_workout_duration": first_course.get("Average Workout Duration", ""),
                "age_group": first_course.get("Age Group", []),
                "gender_orientation": first_course.get("Gender Orientation", ""),
                "physical_limitations": first_course.get("Physical Limitations", []),
                "required_equipment": first_course.get("Required Equipment", []),
                "course_language": first_course.get("Course Language", ""),
                "visual_content": first_course.get("Visual Content", []),
                "trainer_feedback_options": first_course.get("Trainer Feedback Options", []),
                "tags": first_course.get("Tags", []),
                "average_course_rating": first_course.get("Average Course Rating", 0.0),
                "active_participants": first_course.get("Active Participants", 0),
                "number_of_reviews": first_course.get("Number of Reviews", 0),
                "certification": first_course.get("Certification", {}),
                "experience": first_course.get("Experience", {}),
                "trainer_name": first_course.get("Trainer Name", ""),
                "course_title": first_course.get("Course Title", ""),
                "program_description": first_course.get("Program Description", ""),
                "training_plan": first_course.get("training_plan", []),
                "id": first_course.get("id", "")
            }
            
            # Test creating the model
            training = Training(**model_data)
            print(f"✅ Successfully created Training model from JSON data")
            print(f"   Course: {training.course_title}")
            print(f"   Trainer: {training.trainer_name}")
            print(f"   Activity: {training.activity_type}")
            print(f"   Duration: {training.course_duration_weeks} weeks")
            print(f"   Training plan has {len(training.training_plan)} days")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to test with JSON file: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("🧪 Testing New Training Model Structure")
    print("="*60)
    
    success = test_training_model_with_json_data()
    
    if success:
        success = test_with_sample_json_file()
    
    if success:
        print("\n🎉 All tests completed successfully!")
        print("The new Training model is ready to use.")
    else:
        print("\n💥 Some tests failed. Please check the errors above.")
        sys.exit(1) 