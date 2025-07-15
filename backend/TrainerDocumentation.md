# Training and Trainer Models Documentation

Pydantic models for a training management system.

## Core Models

### `Certification`
Model for trainer certifications.

**Fields:**
- `Type: str` - Certification type (ISSA, ACE, NASM, etc.)
- `Level: str` - Certification level (Basic, Advanced, Master)
- `Specialization: str` - Area of specialization

### `Experience`
Model for trainer experience.

**Fields:**
- `Years: int` - Years of experience
- `Specialization: str` - Area of specialization
- `Courses: int` - Number of created courses
- `Rating: float` - Trainer rating

### `Exercise`
Model for individual exercises.

**Fields:**
- `exercise: str` - Exercise name
- `repeats: str` - Number of repetitions
- `sets: str` - Number of sets
- `duration: str` - Duration of exercise
- `rest: str` - Rest time between sets
- `description: str` - Exercise description

### `TrainingDay`
Model for a training day.

**Fields:**
- `title: str` - Training day title
- `exercises: List[Exercise]` - List of exercises

## Main Training Model

### `Training`
Primary training program model.

**Fields:**

**Basic Information:**
- `activity_type: str` - Type of activity
- `program_goal: List[str]` - Program goals
- `training_environment: List[str]` - Training environment
- `difficulty_level: str` - Difficulty level
- `course_duration_weeks: int` - Course duration in weeks
- `weekly_training_frequency: str` - Weekly training frequency
- `average_workout_duration: str` - Average workout duration
- `age_group: List[str]` - Target age group
- `gender_orientation: str` - Gender orientation
- `physical_limitations: List[str]` - Physical limitations
- `required_equipment: List[str]` - Required equipment
- `course_language: str` - Course language
- `visual_content: List[str]` - Visual content types
- `trainer_feedback_options: List[str]` - Trainer feedback options
- `tags: List[str]` - Program tags

**Ratings and Statistics:**
- `average_course_rating: float` - Average course rating
- `active_participants: int` - Active participants count
- `number_of_reviews: int` - Number of reviews

**Trainer Information:**
- `certification: Certification` - Trainer certification
- `experience: Experience` - Trainer experience
- `trainer_name: str` - Trainer name

**Course Information:**
- `course_title: str` - Course title
- `program_description: str` - Program description

**Training Plan:**
- `training_plan: List[TrainingDay]` - Training schedule

**Identifier:**
- `id: str` - Unique course identifier

## CRUD Operation Models

### `TrainingCreate`
Model for creating new training programs. Contains same fields as `Training` with default values.

### `TrainingUpdate`
Model for updating training programs. All fields are optional.

### `TrainingResponse`
Response model with additional fields:
- `db_id: Optional[int]` - Database record ID
- `user_id: Optional[int]` - User ID
- `created_at: Optional[str]` - Creation timestamp
- `updated_at: Optional[str]` - Last update timestamp

## Deprecated Models (for backwards compatibility)

### `Badge`
Model for badges with text and color.

**Fields:**
- `text: str` - Badge text
- `color: str` - Badge color in hex format

### `HeaderBadges`
Model for header badges.

**Fields:**
- `training_type: List[Badge]` - Training type badges
- `training_info: List[Badge]` - Training info badges
- `training_equipment: List[Badge]` - Equipment badges

### `CourseInfo`
Model for course information.

**Fields:**
- `id: str` - Course ID
- `title: str` - Course title
- `author: str` - Course author
- `description: str` - Course description
- `rating: float` - Course rating
- `reviews: int` - Review count

### `CoachData`
Model for coach/trainer data.

**Fields:**
- `name: str` - Trainer name
- `profile_picture: Optional[str]` - Profile picture URL
- `rating: float` - Trainer rating
- `reviews: int` - Review count
- `years: int` - Years of experience
- `badges: List[Badge]` - Trainer badges

### `TrainingMetadata`
Model for training metadata.

**Fields:**
- `tags: Dict[str, Any]` - Training tags
- `certification: Dict[str, Any]` - Certification info
- `experience: Dict[str, Any]` - Experience info

### `LegacyTraining`
Legacy training model for backwards compatibility.

**Fields:**
- `header_badges: HeaderBadges`
- `course_info: CourseInfo`
- `training_plan: List[TrainingDay]`
- `coach_data: CoachData`
- `metadata: TrainingMetadata`

## Additional Models

### `TrainerProfile`
Model for trainer profiles.

**Fields:**
- `profile_picture: Optional[str]` - Profile picture URL
- `certification: Certification` - Trainer certifications
- `experience: Experience` - Trainer experience
- `badges: List[Badge]` - Trainer badges
- `reviews_count: int` - Number of reviews
- `bio: Optional[str]` - Trainer biography

## Backwards Compatibility Aliases
- `TrainerCertification` = `Certification`
- `TrainerExperience` = `Experience`

## User Model Example

Example of a user model (typically used for authentication):

```json
[
    {
        "username": "testcoach",
        "password": "testpassword123",
        "full_name": "Test Coach",
        "email": "test@coach.com",
        "is_admin": true
    }
]
```

