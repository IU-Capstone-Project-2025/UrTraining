# test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app
from models import (
    TrainingUpdate,
    ValidationResponse,
    EditRequest,
    EditResponse,
    Exercise,
    TrainingDay,
    Certification,
    Experience
)
import json

client = TestClient(app)

# Fixtures with test data
@pytest.fixture
def valid_training_data():
    return {
        "Activity Type": "Strength Training",
        "Program Goal": ["Muscle Growth", "Strength"],
        "Training Environment": ["Gym"],
        "Difficulty Level": "Intermediate",
        "Course Duration (weeks)": 8,
        "Weekly Training Frequency": "3 times per week",
        "Average Workout Duration": "60 minutes",
        "Age Group": ["18-35"],
        "Gender Orientation": "Unisex",
        "Physical Limitations": [],
        "Required Equipment": ["Dumbbells", "Barbell"],
        "Course Language": "English",
        "Visual Content": ["Video", "Images"],
        "Trainer Feedback Options": ["Text", "Video"],
        "Tags": ["strength", "hypertrophy"],
        "Average Course Rating": 4.5,
        "Active Participants": 150,
        "Number of Reviews": 30,
        "Certification": {
            "Type": "ACE",
            "Level": "Advanced",
            "Specialization": "Strength Training"
        },
        "Experience": {
            "Years": 5,
            "Specialization": "Strength Training",
            "Courses": 10,
            "Rating": 4.8
        },
        "Trainer Name": "John Doe",
        "Course Title": "Advanced Strength Program",
        "Program Description": "8-week strength training program for intermediates",
        "training_plan": [
            {
                "title": "Day 1: Upper Body",
                "exercises": [
                    {
                        "exercise": "Bench Press",
                        "repeats": "3x5",
                        "sets": "3",
                        "duration": "",
                        "rest": "2 min",
                        "description": "Barbell bench press"
                    }
                ]
            }
        ],
        "id": "test123"
    }

@pytest.fixture
def incomplete_training_data():
    return {
        "Activity Type": "",
        "Program Goal": [],
        "Training Environment": [],
        "Difficulty Level": "",
        "Course Duration (weeks)": 0,
        "Weekly Training Frequency": "",
        "Average Workout Duration": "",
        "Age Group": [],
        "Gender Orientation": "",
        "Physical Limitations": [],
        "Required Equipment": [],
        "Course Language": "",
        "Visual Content": [],
        "Trainer Feedback Options": [],
        "Tags": [],
        "Average Course Rating": 0.0,
        "Active Participants": 0,
        "Number of Reviews": 0,
        "Certification": None,
        "Experience": None,
        "Trainer Name": "",
        "Course Title": "",
        "Program Description": "",
        "training_plan": [],
        "id": "incomplete123"
    }

@pytest.fixture
def edit_request_data(valid_training_data):
    return {
        "training_data": valid_training_data,
        "user_prompt": "Change the difficulty level to Advanced and add a rest day"
    }

# Model tests
def test_training_update_model(valid_training_data):
    training = TrainingUpdate(**valid_training_data)
    assert training.activity_type == "Strength Training"
    assert "Muscle Growth" in training.program_goal
    assert training.certification.Type == "ACE"

def test_validation_response_model():
    valid_response = ValidationResponse(
        status="ok",
        message="All good!"
    )
    assert valid_response.status == "ok"
    
    correction_response = ValidationResponse(
        status="needs_correction",
        requests=["Missing activity type", "Invalid age group"]
    )
    assert len(correction_response.requests) == 2

def test_edit_models(valid_training_data):
    edit_request = EditRequest(
        training_data=TrainingUpdate(**valid_training_data),
        user_prompt="Make changes"
    )
    assert edit_request.user_prompt == "Make changes"
    
    edit_response = EditResponse(
        updated_training_data=TrainingUpdate(**valid_training_data)
    )
    assert edit_response.updated_training_data.course_title == "Advanced Strength Program"

# Endpoint tests
def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Sport Training Program Assistant is running."}

def test_validate_training_endpoint_valid(valid_training_data, mocker):
    # Mock the LLM response
    mock_response = {
        "status": "ok",
        "message": "Great job! All required fields are correctly filled."
    }
    mocker.patch(
        "main.call_kluster_llm",
        return_value=json.dumps(mock_response)
    )
    
    response = client.post(
        "/validate-training/",
        json=valid_training_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_validate_training_endpoint_invalid(incomplete_training_data, mocker):
    # Mock the LLM response
    mock_response = {
        "status": "needs_correction",
        "requests": [
            "Activity Type: Please specify the activity type",
            "Program Goal: At least one goal is required"
        ]
    }
    mocker.patch(
        "main.call_kluster_llm",
        return_value=json.dumps(mock_response)
    )
    
    response = client.post(
        "/validate-training/",
        json=incomplete_training_data
    )
    assert response.status_code == 200
    assert response.json()["status"] == "needs_correction"
    assert len(response.json()["requests"]) == 2

def test_validate_training_endpoint_llm_error(valid_training_data, mocker):
    # Mock invalid LLM response
    mocker.patch(
        "main.call_kluster_llm",
        return_value="invalid json"
    )
    
    response = client.post(
        "/validate-training/",
        json=valid_training_data
    )
    assert response.status_code == 500
    assert "Invalid JSON response from LLM" in response.json()["detail"]

def test_edit_training_endpoint(valid_training_data, edit_request_data, mocker):
    # Mock the LLM response with modified data
    modified_data = valid_training_data.copy()
    modified_data["Difficulty Level"] = "Advanced"
    modified_data["training_plan"].append({
        "title": "Rest Day",
        "exercises": []
    })
    
    mocker.patch(
        "main.call_kluster_llm",
        return_value=json.dumps(modified_data)
    )
    
    response = client.post(
        "/edit-training/",
        json=edit_request_data
    )
    assert response.status_code == 200
    updated_data = response.json()["updated_training_data"]
    assert updated_data["Difficulty Level"] == "Advanced"
    assert len(updated_data["training_plan"]) == 2

def test_edit_training_endpoint_invalid(valid_training_data, mocker):
    # Mock invalid LLM response
    mocker.patch(
        "main.call_kluster_llm",
        return_value="invalid json"
    )
    
    request_data = {
        "training_data": valid_training_data,
        "user_prompt": "Make changes"
    }
    
    response = client.post(
        "/edit-training/",
        json=request_data
    )
    assert response.status_code == 500
    assert "Invalid JSON response from LLM" in response.json()["detail"]

# Utility tests (you'll need to mock the actual API calls)
def test_call_kluster_llm(mocker):
    # This would test your utils.py function if you move it here or import
    pass
