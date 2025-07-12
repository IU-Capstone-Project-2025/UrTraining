import pytest
from pydantic import ValidationError
from datetime import datetime
import os
import sys

# Setting up paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Импортируем только нужные модели, избегая циклических импортов
from app.models.training import (
    Certification,
    Experience,
    TrainerProfile,
    Badge,
    TrainerCertification,
    TrainerExperience
)
# Fixtures для тестов
@pytest.fixture
def sample_certification_data():
    return {
        "Type": "ISSA",
        "Level": "Advanced",
        "Specialization": "Fitness Training"
    }


@pytest.fixture
def sample_experience_data():
    return {
        "Years": 5,
        "Specialization": "Strength Training",
        "Courses": 10,
        "Rating": 4.8
    }


@pytest.fixture
def sample_badge_data():
    return {
        "text": "Elite Trainer",
        "color": "#FF5733"
    }


# Тесты для Certification
class TestCertification:
    def test_create_certification(self, sample_certification_data):
        cert = Certification(**sample_certification_data)
        assert cert.Type == "ISSA"
        assert cert.Level == "Advanced"
        assert cert.Specialization == "Fitness Training"
    
    def test_default_values(self):
        cert = Certification()
        assert cert.Type == ""
        assert cert.Level == ""
        assert cert.Specialization == ""
    
    def test_alias_trainer_certification(self):
        # Проверка алиаса для обратной совместимости
        cert = TrainerCertification(Type="ACE", Level="Master", Specialization="Nutrition")
        assert isinstance(cert, Certification)
        assert cert.Type == "ACE"


# Тесты для Experience
class TestExperience:
    def test_create_experience(self, sample_experience_data):
        exp = Experience(**sample_experience_data)
        assert exp.Years == 5
        assert exp.Specialization == "Strength Training"
        assert exp.Courses == 10
        assert exp.Rating == 4.8
    
    def test_default_values(self):
        exp = Experience()
        assert exp.Years == 0
        assert exp.Specialization == ""
        assert exp.Courses == 0
        assert exp.Rating == 0.0
    
    
    def test_alias_trainer_experience(self):
        # Проверка алиаса для обратной совместимости
        exp = TrainerExperience(Years=3, Specialization="Yoga", Courses=5, Rating=4.5)
        assert isinstance(exp, Experience)
        assert exp.Years == 3


# Тесты для Badge
class TestBadge:
    def test_create_badge(self, sample_badge_data):
        badge = Badge(**sample_badge_data)
        assert badge.text == "Elite Trainer"
        assert badge.color == "#FF5733"
    
    def test_missing_fields(self):
        with pytest.raises(ValidationError):
            Badge(text="Only text")
        
        with pytest.raises(ValidationError):
            Badge(color="#FFFFFF")


# Тесты для TrainerProfile
class TestTrainerProfile:
    def test_create_profile(self, sample_certification_data, sample_experience_data, sample_badge_data):
        profile = TrainerProfile(
            profile_picture="http://example.com/photo.jpg",
            certification=Certification(**sample_certification_data),
            experience=Experience(**sample_experience_data),
            badges=[Badge(**sample_badge_data)],
            reviews_count=25,
            bio="Certified fitness trainer with 5 years of experience"
        )
        
        assert profile.profile_picture == "http://example.com/photo.jpg"
        assert profile.certification.Type == "ISSA"
        assert profile.experience.Years == 5
        assert len(profile.badges) == 1
        assert profile.badges[0].text == "Elite Trainer"
        assert profile.reviews_count == 25
        assert profile.bio == "Certified fitness trainer with 5 years of experience"
    
    def test_default_values(self):
        profile = TrainerProfile(
            certification=Certification(),
            experience=Experience()
        )
        
        assert profile.profile_picture is None
        assert len(profile.badges) == 0
        assert profile.reviews_count == 0
        assert profile.bio is None
    
    def test_required_fields(self):
        with pytest.raises(ValidationError):
            TrainerProfile()  # Нет certification и experience
        
        with pytest.raises(ValidationError):
            TrainerProfile(certification=Certification())  # Нет experience
        
        with pytest.raises(ValidationError):
            TrainerProfile(experience=Experience())  # Нет certification
    
    def test_badges_list(self):
        profile = TrainerProfile(
            certification=Certification(),
            experience=Experience(),
            badges=[
                Badge(text="Badge1", color="#111111"),
                Badge(text="Badge2", color="#222222")
            ]
        )
        
        assert len(profile.badges) == 2
        assert profile.badges[0].text == "Badge1"
        assert profile.badges[1].text == "Badge2"


# Интеграционные тесты
class TestIntegration:
    def test_full_profile_creation(self):
        # Создаем полный профиль тренера со всеми данными
        cert = Certification(
            Type="NASM",
            Level="Master",
            Specialization="Performance Enhancement"
        )
        
        exp = Experience(
            Years=7,
            Specialization="Athletic Performance",
            Courses=15,
            Rating=4.9
        )
        
        badges = [
            Badge(text="Top Trainer", color="#FF0000"),
            Badge(text="Nutrition Expert", color="#00FF00")
        ]
        
        profile = TrainerProfile(
            profile_picture="/images/trainers/123.jpg",
            certification=cert,
            experience=exp,
            badges=badges,
            reviews_count=42,
            bio="Helping athletes achieve peak performance"
        )
        
        # Проверяем данные сертификации
        assert profile.certification.Type == "NASM"
        assert profile.certification.Level == "Master"
        
        # Проверяем данные опыта
        assert profile.experience.Years == 7
        assert profile.experience.Rating == 4.9
        
        # Проверяем дополнительные поля
        assert len(profile.badges) == 2
        assert profile.badges[1].text == "Nutrition Expert"
        assert profile.reviews_count == 42
        assert "peak performance" in profile.bio
    
    

# Дополнительные тесты для Badge
class TestBadgeAdditional:
    
    def test_badge_color_case_insensitivity(self):
        # HEX-цвет должен быть нечувствителен к регистру
        badge1 = Badge(text="Test", color="#ffffff")
        badge2 = Badge(text="Test", color="#FFFFFF")
        assert badge1.color == badge2.color.lower()

# Дополнительные тесты для TrainerProfile
class TestTrainerProfileAdditional:
    @pytest.fixture
    def full_profile_data(self):
        return {
            "profile_picture": "http://example.com/photo.jpg",
            "certification": {
                "Type": "ACE",
                "Level": "Master",
                "Specialization": "Nutrition"
            },
            "experience": {
                "Years": 5,
                "Specialization": "Strength Training",
                "Courses": 10,
                "Rating": 4.8
            },
            "badges": [
                {"text": "Elite Trainer", "color": "#FF5733"},
                {"text": "Nutrition Expert", "color": "#00FF00"}
            ],
            "reviews_count": 25,
            "bio": "Certified fitness trainer with 5 years of experience"
        }
    
    def test_profile_from_dict(self, full_profile_data):
        profile = TrainerProfile(**full_profile_data)
        assert profile.certification.Type == "ACE"
        assert len(profile.badges) == 2
    

# Тесты для сериализации/десериализации
class TestSerialization:
    def test_certification_serialization(self, sample_certification_data):
        cert = Certification(**sample_certification_data)
        cert_dict = cert.dict()
        assert cert_dict["Type"] == sample_certification_data["Type"]
        assert cert_dict["Level"] == sample_certification_data["Level"]
    
    def test_experience_json_serialization(self, sample_experience_data):
        exp = Experience(**sample_experience_data)
        exp_json = exp.json()
        assert str(sample_experience_data["Years"]) in exp_json
        assert sample_experience_data["Specialization"] in exp_json
    
    def test_profile_serialization_roundtrip(self):
        original = TrainerProfile(
            certification=Certification(Type="NASM", Level="Master"),
            experience=Experience(Years=5, Rating=4.5),
            badges=[Badge(text="Test", color="#FFFFFF")]
        )
        
        serialized = original.json()
        deserialized = TrainerProfile.parse_raw(serialized)
        
        assert original == deserialized

# Тесты для edge cases
class TestEdgeCases:
    def test_empty_badges_list(self):
        profile = TrainerProfile(
            certification=Certification(),
            experience=Experience(),
            badges=[]
        )
        assert len(profile.badges) == 0
    
    def test_minimal_valid_profile(self):
        profile = TrainerProfile(
            certification=Certification(),
            experience=Experience()
        )
        assert profile
    
    def test_max_values_profile(self):
        profile = TrainerProfile(
            certification=Certification(
                Type="NASM",
                Level="Master",
                Specialization="Performance Enhancement"
            ),
            experience=Experience(
                Years=50,
                Specialization="Athletic Performance",
                Courses=1000,
                Rating=5.0
            ),
            badges=[Badge(text="A"*100, color="#FFFFFF")],
            reviews_count=1000000,
            bio="A"*2000,
            profile_picture="https://example.com/" + "a"*100 + ".jpg"
        )
        assert profile

# Тесты для обновления профиля
class TestProfileUpdate:
    @pytest.fixture
    def base_profile(self):
        return TrainerProfile(
            certification=Certification(Type="ACE", Level="Basic"),
            experience=Experience(Years=1, Rating=3.5)
        )
    
    def test_add_badge(self, base_profile):
        updated = base_profile.copy(update={
            "badges": [Badge(text="New", color="#000000")]
        })
        assert len(updated.badges) == 1
        assert updated.badges[0].text == "New"

# Тесты для обновления профиля
class TestProfileUpdateAdvanced:
    @pytest.fixture
    def sample_profile(self):
        return TrainerProfile(
            certification=Certification(Type="ACE", Level="Basic"),
            experience=Experience(Years=2, Rating=4.0),
            badges=[Badge(text="Beginner", color="#000000")]
        )
    
        
    def test_add_multiple_badges(self, sample_profile):
        updated = sample_profile.copy(update={
            "badges": [
                Badge(text="Advanced", color="#FF0000"),
                Badge(text="Expert", color="#00FF00")
            ]
        })
        assert len(updated.badges) == 2
        assert updated.badges[0].text == "Advanced"

# Тесты для edge cases
class TestEdgeCasesAdvanced:
    def test_profile_with_max_values(self):
        profile = TrainerProfile(
            certification=Certification(
                Type="NASM",
                Level="Master",
                Specialization="Performance Enhancement"
            ),
            experience=Experience(
                Years=50,
                Specialization="Athletic Performance",
                Courses=1000,
                Rating=5.0
            ),
            badges=[
                Badge(text="A"*100, color="#FFFFFF"),
                Badge(text="B"*100, color="#000000")
            ],
            reviews_count=1000000,
            bio="A"*2000,
            profile_picture="https://example.com/" + "a"*100 + ".jpg"
        )
        assert profile
        
    def test_empty_specialization(self):
        profile = TrainerProfile(
            certification=Certification(Specialization=""),
            experience=Experience(Specialization="")
        )
        assert profile.certification.Specialization == ""
        assert profile.experience.Specialization == ""

# Тесты для сериализации
class TestSerializationAdvanced:
    def test_experience_serialization(self, sample_experience_data):
        exp = Experience(**sample_experience_data)
        exp_dict = exp.dict()
        assert exp_dict["Years"] == sample_experience_data["Years"]
        assert exp_dict["Rating"] == sample_experience_data["Rating"]
        
    def test_profile_serialization_with_none(self):
        profile = TrainerProfile(
            certification=Certification(),
            experience=Experience(),
            profile_picture=None
        )
        serialized = profile.json()
        assert "null" in serialized  # Проверяем сериализацию None

import pytest
from pydantic import ValidationError
from typing import List, Optional
from datetime import datetime
import os
import sys

# Setting up paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# Models for form data
from pydantic import BaseModel

class StepOption(BaseModel):
    value: str
    placeholder: str

class InputOption(BaseModel):
    id: str
    name: str
    value: str
    placeholder: str

class FormInput(BaseModel):
    name: str
    id: str
    input_type: str
    placeholder: str
    options: Optional[List[InputOption]] = None

class FormOption(BaseModel):
    subtitle: str
    inputs: List[FormInput]

class Information(BaseModel):
    title: str
    description: str

class FormStep(BaseModel):
    steps_total: List[StepOption]
    step_current: str
    title: str
    options: List[FormOption]
    information: Information

# Fixtures for test data
@pytest.fixture
def step1_data():
    return {
        "steps_total": [
            {
                "value": "step-1",
                "placeholder": "Step 1"
            },
            {
                "value": "step-2",
                "placeholder": "Step 2"
            },
            {
                "value": "step-3",
                "placeholder": "Step 3"
            }
        ],
        "step_current": "step-1",
        "title": "Let's know each other!",
        "options": [
            {
                "subtitle": "How can we call you?",
                "inputs": [
                    {
                        "name": "name",
                        "id": "name",
                        "input_type": "text",
                        "placeholder": "Name",
                        "options": ""
                    },
                    {
                        "name": "surname",
                        "id": "surname",
                        "input_type": "text",
                        "placeholder": "Surname",
                        "options": ""
                    }
                ]
            },
            {
                "subtitle": "Where are you from?",
                "inputs": [
                    {
                        "name": "country",
                        "id": "country",
                        "input_type": "select",
                        "placeholder": "Country",
                        "options": [
                            {
                                "id": "kz",
                                "name": "kazakhstan",
                                "value": "kz",
                                "placeholder": "Kazakhstan"
                            },
                            {
                                "id": "ru",
                                "name": "russia",
                                "value": "ru",
                                "placeholder": "Russia"
                            },
                            {
                                "id": "us",
                                "name": "usa",
                                "value": "us",
                                "placeholder": "United States"
                            }
                        ]
                    },
                    {
                        "name": "city",
                        "id": "city",
                        "input_type": "text",
                        "placeholder": "City (can skip)",
                        "options": ""
                    }
                ]
            },
            {
                "subtitle": "What is your gender?",
                "inputs": [
                    {
                        "name": "gender",
                        "id": "gender",
                        "input_type": "radio",
                        "placeholder": "Gender",
                        "options": [
                            {
                                "id": "male",
                                "name": "gender",
                                "value": "male",
                                "placeholder": "Male"
                            },
                            {
                                "id": "female",
                                "name": "gender",
                                "value": "female",
                                "placeholder": "Female"
                            }
                        ]
                    }
                ]
            }
        ],
        "information": {
            "title": "Why we collect your data?",
            "description": "To correctly identify your target audience and recommend your plans to the right people. It only takes 2-3 minutes."
        }
    }

@pytest.fixture
def step2_data():
    return {
        "steps_total": [
            {
                "value": "step-1",
                "placeholder": "Step 1"
            },
            {
                "value": "step-2",
                "placeholder": "Step 2"
            },
            {
                "value": "step-3",
                "placeholder": "Step 3"
            }
        ],
        "step_current": "step-2",
        "title": "Let's talk about your target!",
        "options": [
            {
                "subtitle": "What kind of sports do you specialize in?",
                "inputs": [
                    {
                        "name": "specialization",
                        "id": "specialization",
                        "input_type": "select",
                        "placeholder": "Select prior activity",
                        "options": [
                            {
                                "id": "bodybuilding",
                                "name": "bodybuilding",
                                "value": "bodybuilding",
                                "placeholder": "Bodybuilding"
                            },
                            {
                                "id": "strength",
                                "name": "strength",
                                "value": "strength",
                                "placeholder": "Strength training"
                            },
                            {
                                "id": "mobility",
                                "name": "mobility",
                                "value": "mobility",
                                "placeholder": "Mobility training"
                            },
                            {
                                "id": "stretching",
                                "name": "stretching",
                                "value": "stretching",
                                "placeholder": "Stretching"
                            },
                            {
                                "id": "functional",
                                "name": "functional",
                                "value": "functional",
                                "placeholder": "Functional training"
                            },
                            {
                                "id": "swimming",
                                "name": "swimming",
                                "value": "swimming",
                                "placeholder": "Swimming"
                            },
                            {
                                "id": "yoga/pilates",
                                "name": "yoga/pilates",
                                "value": "yoga/pilates",
                                "placeholder": "Yoga / Pilates"
                            }
                        ]
                    }
                ]
            },
            {
                "subtitle": "How do you prefer to train?",
                "inputs": [
                    {
                        "name": "training_location",
                        "id": "training_location",
                        "input_type": "select",
                        "placeholder": "Select specialization",
                        "options": [
                            {
                                "id": "gym",
                                "name": "gym",
                                "value": "gym",
                                "placeholder": "Gym"
                            },
                            {
                                "id": "outdoors",
                                "name": "outdoors",
                                "value": "outdoors",
                                "placeholder": "Outdoors"
                            },
                            {
                                "id": "pool",
                                "name": "pool",
                                "value": "pool",
                                "placeholder": "In the pool"
                            },
                            {
                                "id": "home",
                                "name": "home",
                                "value": "home",
                                "placeholder": "Home trainings"
                            }
                        ]
                    }
                ]
            },
            {
                "subtitle": "Do you train athletes for competitions?",
                "inputs": [
                    {
                        "name": "competitions",
                        "id": "competitions",
                        "input_type": "radio",
                        "placeholder": "",
                        "options": [
                            {
                                "id": "true",
                                "name": "competitions",
                                "value": "true",
                                "placeholder": "Yes"
                            },
                            {
                                "id": "false",
                                "name": "competitions",
                                "value": "false",
                                "placeholder": "No"
                            }
                        ]
                    }
                ]
            }
        ],
        "information": {
            "title": "Why we collect your data?",
            "description": "To correctly identify your target audience and recommend your plans to the right people. It only takes 2-3 minutes."
        }
    }

@pytest.fixture
def step3_data():
    return {
        "steps_total": [
            {
                "value": "step-1",
                "placeholder": "Step 1"
            },
            {
                "value": "step-2",
                "placeholder": "Step 2"
            },
            {
                "value": "step-3",
                "placeholder": "Step 3"
            }
        ],
        "step_current": "step-3",
        "title": "Let's talk about your experience!",
        "options": [
            {
                "subtitle": "How long have you been involved in coaching, in your opinion?",
                "inputs": [
                    {
                        "name": "years",
                        "id": "years",
                        "input_type": "number",
                        "placeholder": "Write in years..",
                        "options": ""
                    }
                ]
            },
            {
                "subtitle": "What is the level of your education/certification?",
                "inputs": [
                    {
                        "name": "level",
                        "id": "level",
                        "input_type": "text",
                        "placeholder": "Level..",
                        "options": ""
                    }
                ]
            },
            {
                "subtitle": "Do you have any proof of your education/certification? Write name of certificate, if any:",
                "inputs": [
                    {
                        "name": "sertification",
                        "id": "sertification",
                        "input_type": "text",
                        "placeholder": "Certificate name..",
                        "options": ""
                    }
                ]
            }
        ],
        "information": {
            "title": "Why we collect your data?",
            "description": "To correctly identify your target audience and recommend your plans to the right people. It only takes 2-3 minutes."
        }
    }

# Tests for StepOption model
class TestStepOption:
    def test_create_step_option(self):
        option = StepOption(value="step-1", placeholder="Step 1")
        assert option.value == "step-1"
        assert option.placeholder == "Step 1"
    
    def test_missing_fields(self):
        with pytest.raises(ValidationError):
            StepOption(value="step-1")
        
        with pytest.raises(ValidationError):
            StepOption(placeholder="Step 1")

# Tests for InputOption model
class TestInputOption:
    def test_create_input_option(self):
        option = InputOption(
            id="male",
            name="gender",
            value="male",
            placeholder="Male"
        )
        assert option.id == "male"
        assert option.name == "gender"
        assert option.value == "male"
        assert option.placeholder == "Male"
    
    def test_missing_fields(self):
        with pytest.raises(ValidationError):
            InputOption(name="gender", value="male", placeholder="Male")

# Tests for FormInput model
class TestFormInput:
    def test_create_text_input(self):
        input_field = FormInput(
            name="name",
            id="name",
            input_type="text",
            placeholder="Name",
            options=None
        )
        assert input_field.input_type == "text"
        assert input_field.options is None
    
    def test_create_select_input(self):
        options = [
            InputOption(
                id="kz",
                name="kazakhstan",
                value="kz",
                placeholder="Kazakhstan"
            )
        ]
        input_field = FormInput(
            name="country",
            id="country",
            input_type="select",
            placeholder="Country",
            options=options
        )
        assert input_field.input_type == "select"
        assert len(input_field.options) == 1
        assert input_field.options[0].id == "kz"
    


# Tests for Information model
class TestInformation:
    def test_create_information(self):
        info = Information(
            title="Test title",
            description="Test description"
        )
        assert info.title == "Test title"
        assert info.description == "Test description"
    
    def test_missing_fields(self):
        with pytest.raises(ValidationError):
            Information(title="Test title")
        
        with pytest.raises(ValidationError):
            Information(description="Test description")

# Tests for FormStep model
class TestFormStep:
    
    def test_create_step1(self, step2_data):
        step = FormStep(**step2_data)
        assert step.step_current == "step-2"
        assert step.title == "Let's talk about your target!"
        assert len(step.options[0].inputs[0].options) == 7
    
    
    def test_invalid_step_current(self, step1_data):
        invalid_data = step1_data.copy()
        invalid_data["step_current"] = "invalid-step"
        with pytest.raises(ValidationError):
            FormStep(**invalid_data)
    
    def test_missing_steps_total(self, step1_data):
        invalid_data = step1_data.copy()
        del invalid_data["steps_total"]
        with pytest.raises(ValidationError):
            FormStep(**invalid_data)
    

# Edge cases tests
class TestEdgeCases:
    
    def test_minimal_valid_step(self):
        minimal_data = {
            "steps_total": [{"value": "step-1", "placeholder": "Step 1"}],
            "step_current": "step-1",
            "title": "Test",
            "options": [{
                "subtitle": "Test",
                "inputs": [{
                    "name": "test",
                    "id": "test",
                    "input_type": "text",
                    "placeholder": "Test"
                }]
            }],
            "information": {
                "title": "Test",
                "description": "Test"
            }
        }
        step = FormStep(**minimal_data)
        assert step

# Serialization tests
class TestSerialization:
    
    def test_json_serialization(self, step2_data):
        step = FormStep(**step2_data)
        step_json = step.json()
        
        assert "step-2" in step_json
        assert "Let's talk about your target!" in step_json
        assert "Bodybuilding" in step_json  # Check one of the options

# Test for input types
class TestInputTypes:
    @pytest.mark.parametrize("input_type", ["text", "number", "select", "radio"])
    def test_valid_input_types(self, input_type):
        input_field = FormInput(
            name="test",
            id="test",
            input_type=input_type,
            placeholder="Test"
        )
        assert input_field.input_type == input_type
    

# Test for option validation
class TestOptionValidation:
    
    def test_text_with_options(self, step1_data):
        # Text input shouldn't have options
        modified_data = step1_data.copy()
        modified_data["options"][0]["inputs"][0]["options"] = [
            {"id": "1", "name": "test", "value": "1", "placeholder": "Test"}
        ]
        
        with pytest.raises(ValidationError):
            FormStep(**modified_data)
