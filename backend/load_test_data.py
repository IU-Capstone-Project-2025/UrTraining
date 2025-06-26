#!/usr/bin/env python3
"""
Script to load test training data from selected_courses_with_ids_plus_plan.json
This script sends POST request to /trainings/list endpoint to populate the database
"""

import json
import requests
import time
import os
import sys
from typing import Dict, Any

# Configuration
API_BASE_URL = "http://localhost:8000"
TRAININGS_ENDPOINT = "/trainings/list"
TEST_DATA_FILE = "selected_courses_with_ids_plus_plan.json"
AUTH_DATA_FILE = "data/test_coach_auth.json"

def wait_for_api(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for API to be available"""
    print("Waiting for API to be available...")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{API_BASE_URL}/docs", timeout=5)
            if response.status_code == 200:
                print("API is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"Attempt {attempt + 1}/{max_retries} - API not ready yet, waiting {delay} seconds...")
        time.sleep(delay)
    
    print("API failed to become available within timeout")
    return False

def register_test_coach(coach_data: Dict[str, Any]) -> bool:
    """Register test coach if not exists"""
    try:
        # Try to register the coach
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json=coach_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("Test coach registered successfully!")
            return True
        elif response.status_code == 400 and "already exists" in response.text:
            print("Test coach already exists")
            return True
        else:
            print(f"Failed to register test coach: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"Error registering test coach: {e}")
        return False

def get_auth_token() -> str:
    """Get authentication token from coach auth data"""
    try:
        with open(AUTH_DATA_FILE, 'r', encoding='utf-8') as f:
            auth_data = json.load(f)
        
        # Use first coach for authentication
        if not auth_data:
            raise ValueError("No coach data found in auth file")
        
        coach = auth_data[0]
        
        # Try to register the coach first
        if not register_test_coach(coach):
            print("Warning: Could not register test coach, but continuing...")
        
        # Login to get token
        login_data = {
            "email": coach["email"],
            "password": coach["password"]
        }
        
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get("access_token")
        else:
            print(f"Failed to login: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error getting auth token: {e}")
        return None

def load_test_data() -> bool:
    """Load test data from JSON file and send to API"""
    try:
        # Check if test data file exists
        if not os.path.exists(TEST_DATA_FILE):
            print(f"Test data file not found: {TEST_DATA_FILE}")
            return False
        
        # Load test data
        print(f"Loading test data from {TEST_DATA_FILE}...")
        with open(TEST_DATA_FILE, 'r', encoding='utf-8') as f:
            trainings_data = json.load(f)
        
        print(f"Found {len(trainings_data)} training programs to load")
        
        # Get authentication token
        auth_token = get_auth_token()
        if not auth_token:
            print("Failed to get authentication token")
            return False
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {auth_token}"
        }
        
        # Convert data to match API expectations
        api_data = []
        for training in trainings_data:
            # Map fields from JSON to API format
            api_training = {
                "activity_type": training.get("Activity Type", ""),
                "program_goal": training.get("Program Goal", []),
                "training_environment": training.get("Training Environment", []),
                "difficulty_level": training.get("Difficulty Level", ""),
                "course_duration_weeks": training.get("Course Duration (weeks)", 0),
                "weekly_training_frequency": training.get("Weekly Training Frequency", ""),
                "average_workout_duration": training.get("Average Workout Duration", ""),
                "age_group": training.get("Age Group", []),
                "gender_orientation": training.get("Gender Orientation", ""),
                "physical_limitations": training.get("Physical Limitations", []),
                "required_equipment": training.get("Required Equipment", []),
                "course_language": training.get("Course Language", ""),
                "visual_content": training.get("Visual Content", []),
                "trainer_feedback_options": training.get("Trainer Feedback Options", []),
                "tags": training.get("Tags", []),
                "average_course_rating": training.get("Average Course Rating", 0.0),
                "active_participants": training.get("Active Participants", 0),
                "number_of_reviews": training.get("Number of Reviews", 0),
                "certification": training.get("Certification", {}),
                "experience": training.get("Experience", {}),
                "trainer_name": training.get("Trainer Name", ""),
                "course_title": training.get("Course Title", ""),
                "program_description": training.get("Program Description", ""),
                "training_plan": training.get("training_plan", []),
                "course_id": training.get("id", "")
            }
            api_data.append(api_training)
        
        # Check if data already exists
        print("Checking if test data already exists...")
        check_response = requests.get(
            f"{API_BASE_URL}/trainings",
            headers=headers,
            timeout=30
        )
        
        if check_response.status_code == 200:
            existing_trainings = check_response.json()
            if existing_trainings and len(existing_trainings) > 0:
                print(f"Found {len(existing_trainings)} existing training programs. Skipping data load.")
                return True
        
        # Send POST request to API
        print(f"Sending data to {API_BASE_URL}{TRAININGS_ENDPOINT}...")
        response = requests.post(
            f"{API_BASE_URL}{TRAININGS_ENDPOINT}",
            json=api_data,
            headers=headers,
            timeout=120  # 2 minutes timeout for large data
        )
        
        if response.status_code == 200:
            print("Test data loaded successfully!")
            return True
        else:
            print(f"Failed to load test data: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error loading test data: {e}")
        return False

def main():
    """Main function"""
    print("Starting test data loading process...")
    
    # Wait for API to be available
    if not wait_for_api():
        print("Exiting due to API unavailability")
        sys.exit(1)
    
    # Load test data
    if load_test_data():
        print("Test data loading completed successfully!")
        sys.exit(0)
    else:
        print("Test data loading failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 