from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
import re


# Enums for validation
class CertificationType(str, Enum):
    """Допустимые типы сертификации"""
    ISSA = "ISSA"
    ACE = "ACE"
    NASM = "NASM"
    ACSM = "ACSM"
    NSCA = "NSCA"
    CSCS = "CSCS"
    PTA_GLOBAL = "PTA Global"
    OTHER = "Other"


class CertificationLevel(str, Enum):
    """Допустимые уровни сертификации"""
    BASIC = "Basic"
    INTERMEDIATE = "Intermediate"
    ADVANCED = "Advanced"
    MASTER = "Master"
    EXPERT = "Expert"


class TrainerSpecialization(str, Enum):
    """Допустимые специализации тренера"""
    STRENGTH_TRAINING = "Strength Training"
    CARDIO_TRAINING = "Cardio Training"
    HIIT = "HIIT"
    YOGA = "Yoga"
    PILATES = "Pilates"
    FUNCTIONAL_TRAINING = "Functional Training"
    CROSSFIT = "CrossFit"
    BODYBUILDING = "Bodybuilding"
    POWERLIFTING = "Powerlifting"
    OLYMPIC_WEIGHTLIFTING = "Olympic Weightlifting"
    SPORTS_PERFORMANCE = "Sports Performance"
    REHABILITATION = "Rehabilitation"
    NUTRITION_COACHING = "Nutrition Coaching"
    GROUP_FITNESS = "Group Fitness"
    PERSONAL_TRAINING = "Personal Training"
    MARTIAL_ARTS = "Martial Arts"
    SWIMMING = "Swimming"
    RUNNING_ENDURANCE = "Running/Endurance"
    FLEXIBILITY_STRETCHING = "Flexibility/Stretching"
    WEIGHT_LOSS = "Weight Loss"
    MUSCLE_GAIN = "Muscle Gain"
    SENIOR_FITNESS = "Senior Fitness"
    YOUTH_FITNESS = "Youth Fitness"
    PRENATAL_POSTNATAL = "Pre/Postnatal Fitness"
    OTHER = "Other"


class Certification(BaseModel):
    """Модель для сертификации тренера"""
    Type: CertificationType = Field(..., description="Тип сертификации (ISSA, ACE, NASM и т.д.)")
    Level: CertificationLevel = Field(..., description="Уровень сертификации (Basic, Advanced, Master)")
    
    @validator('Type')
    def validate_type(cls, v):
        if not v or (isinstance(v, str) and not v.strip()):
            raise ValueError('Certification type is required')
        return v
    
    @validator('Level')
    def validate_level(cls, v):
        if not v or (isinstance(v, str) and not v.strip()):
            raise ValueError('Certification level is required')
        return v
    
    class Config:
        use_enum_values = True


class Experience(BaseModel):
    """Модель для опыта тренера"""
    Years: int = Field(..., ge=0, le=50, description="Количество лет опыта (0-50)")
    Specialization: str = Field(..., min_length=2, max_length=200, description="Специализация")
    Courses: int = Field(..., ge=0, le=10000, description="Количество созданных курсов (0-10000)")
    Rating: float = Field(..., ge=0.0, le=5.0, description="Рейтинг тренера (0.0-5.0)")
    
    @validator('Years')
    def validate_years(cls, v):
        if v < 0 or v > 50:
            raise ValueError('Years of experience must be between 0 and 50')
        return v
    
    @validator('Specialization')
    def validate_specialization(cls, v):
        if not v or not v.strip():
            raise ValueError('Experience specialization is required')
        
        v = v.strip()
        
        # Проверка формата - разрешены буквы, цифры, пробелы, дефисы, запятые, точки
        pattern = r'^[a-zA-Zа-яА-Я0-9\s\-,\.]+$'
        if not re.match(pattern, v):
            raise ValueError('Invalid specialization format')
        
        # Разбираем специализации по запятым и проверяем каждую
        specializations = [spec.strip() for spec in v.split(',')]
        
        if len(specializations) > 5:
            raise ValueError('Too many specializations (max 5)')
        
        # Проверяем на дубликаты
        if len(specializations) != len(set(spec.lower() for spec in specializations)):
            raise ValueError('Duplicate specializations not allowed')
        
        # Проверяем, что каждая специализация из допустимого списка
        valid_specializations = [spec.value.lower() for spec in TrainerSpecialization]
        
        for spec in specializations:
            if spec.lower().strip() not in valid_specializations:
                allowed_values = ', '.join([s.value for s in TrainerSpecialization])
                raise ValueError(f'Invalid specialization "{spec}". Allowed values: {allowed_values}')
        
        return v
    
    @validator('Courses')
    def validate_courses(cls, v):
        if v < 0 or v > 10000:
            raise ValueError('Number of courses must be between 0 and 10000')
        return v
    
    @validator('Rating')
    def validate_rating(cls, v):
        if v < 0.0 or v > 5.0:
            raise ValueError('Rating must be between 0.0 and 5.0')
        # Округляем до 1 знака после запятой
        return round(v, 1)
    
    # Cross-field валидация
    @validator('Rating')
    def validate_rating_vs_years(cls, v, values):
        years = values.get('Years', 0)
        if years < 1 and v > 3.0:
            raise ValueError('Rating cannot be higher than 3.0 for trainers with less than 1 year of experience')
        return v
    
    @validator('Courses')
    def validate_courses_vs_years(cls, v, values):
        years = values.get('Years', 0)
        if years > 0 and v > years * 10:  # Более мягкое ограничение
            raise ValueError(f'Number of courses ({v}) seems inconsistent with years of experience ({years})')
        return v
    
    class Config:
        use_enum_values = True


class Exercise(BaseModel):
    """Модель для упражнения"""
    exercise: str = Field(default="", description="Название упражнения")
    repeats: str = Field(default="", description="Количество повторений")
    sets: str = Field(default="", description="Количество подходов")
    duration: str = Field(default="", description="Продолжительность")
    rest: str = Field(default="", description="Время отдыха")
    description: str = Field(default="", description="Описание упражнения")
    
    class Config:
        use_enum_values = True


class TrainingDay(BaseModel):
    """Модель для тренировочного дня"""
    title: str = Field(default="", description="Название дня тренировки")
    exercises: List[Exercise] = Field(default_factory=list, description="Список упражнений")
    
    class Config:
        use_enum_values = True


class Training(BaseModel):
    """
    Основная модель тренировки, соответствующая структуре JSON с курсами
    """
    # Основная информация о курсе
    activity_type: str = Field(..., alias="Activity Type", description="Тип активности")
    program_goal: List[str] = Field(..., alias="Program Goal", description="Цели программы")
    training_environment: List[str] = Field(..., alias="Training Environment", description="Среда тренировок")
    difficulty_level: str = Field(..., alias="Difficulty Level", description="Уровень сложности")
    course_duration_weeks: int = Field(..., alias="Course Duration (weeks)", description="Продолжительность курса в неделях")
    weekly_training_frequency: str = Field(..., alias="Weekly Training Frequency", description="Частота тренировок в неделю")
    average_workout_duration: str = Field(..., alias="Average Workout Duration", description="Средняя продолжительность тренировки")
    age_group: List[str] = Field(..., alias="Age Group", description="Возрастная группа")
    gender_orientation: str = Field(..., alias="Gender Orientation", description="Гендерная ориентация")
    physical_limitations: List[str] = Field(..., alias="Physical Limitations", description="Физические ограничения")
    required_equipment: List[str] = Field(..., alias="Required Equipment", description="Необходимое оборудование")
    course_language: str = Field(..., alias="Course Language", description="Язык курса")
    visual_content: List[str] = Field(..., alias="Visual Content", description="Визуальный контент")
    trainer_feedback_options: List[str] = Field(..., alias="Trainer Feedback Options", description="Варианты обратной связи от тренера")
    tags: List[str] = Field(..., alias="Tags", description="Теги")
    
    # Рейтинги и статистика
    average_course_rating: float = Field(..., alias="Average Course Rating", description="Средний рейтинг курса")
    active_participants: int = Field(..., alias="Active Participants", description="Активные участники")
    number_of_reviews: int = Field(..., alias="Number of Reviews", description="Количество отзывов")
    
    # Данные о тренере
    certification: Certification = Field(..., alias="Certification", description="Сертификация тренера")
    experience: Experience = Field(..., alias="Experience", description="Опыт тренера")
    trainer_name: str = Field(..., alias="Trainer Name", description="Имя тренера")
    
    # Информация о курсе
    course_title: str = Field(..., alias="Course Title", description="Название курса")
    program_description: str = Field(..., alias="Program Description", description="Описание программы")
    
    # План тренировок
    training_plan: List[TrainingDay] = Field(..., alias="training_plan", description="План тренировок")
    
    # ID курса
    id: str = Field(..., description="Уникальный идентификатор курса")
    
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True


class TrainingCreate(BaseModel):
    """Модель для создания новой тренировки"""
    activity_type: str = Field(default="", alias="Activity Type", description="Тип активности")
    program_goal: List[str] = Field(default_factory=list, alias="Program Goal", description="Цели программы")
    training_environment: List[str] = Field(default_factory=list, alias="Training Environment", description="Среда тренировок")
    difficulty_level: str = Field(default="", alias="Difficulty Level", description="Уровень сложности")
    course_duration_weeks: int = Field(default=0, alias="Course Duration (weeks)", description="Продолжительность курса в неделях")
    weekly_training_frequency: str = Field(default="", alias="Weekly Training Frequency", description="Частота тренировок в неделю")
    average_workout_duration: str = Field(default="", alias="Average Workout Duration", description="Средняя продолжительность тренировки")
    age_group: List[str] = Field(default_factory=list, alias="Age Group", description="Возрастная группа")
    gender_orientation: str = Field(default="", alias="Gender Orientation", description="Гендерная ориентация")
    physical_limitations: List[str] = Field(default_factory=list, alias="Physical Limitations", description="Физические ограничения")
    required_equipment: List[str] = Field(default_factory=list, alias="Required Equipment", description="Необходимое оборудование")
    course_language: str = Field(default="", alias="Course Language", description="Язык курса")
    visual_content: List[str] = Field(default_factory=list, alias="Visual Content", description="Визуальный контент")
    trainer_feedback_options: List[str] = Field(default_factory=list, alias="Trainer Feedback Options", description="Варианты обратной связи от тренера")
    tags: List[str] = Field(default_factory=list, alias="Tags", description="Теги")
    
    # Рейтинги и статистика с дефолтными значениями
    average_course_rating: float = Field(default=0.0, alias="Average Course Rating", description="Средний рейтинг курса")
    active_participants: int = Field(default=0, alias="Active Participants", description="Активные участники")
    number_of_reviews: int = Field(default=0, alias="Number of Reviews", description="Количество отзывов")
    
    # Данные о тренере с дефолтными значениями
    certification: Optional[Certification] = Field(default=None, alias="Certification", description="Сертификация тренера")
    experience: Optional[Experience] = Field(default=None, alias="Experience", description="Опыт тренера")
    trainer_name: str = Field(default="", alias="Trainer Name", description="Имя тренера")
    
    # Информация о курсе
    course_title: str = Field(default="", alias="Course Title", description="Название курса")
    program_description: str = Field(default="", alias="Program Description", description="Описание программы")
    
    # План тренировок
    training_plan: List[TrainingDay] = Field(default_factory=list, alias="training_plan", description="План тренировок")
    
    # ID курса (опциональный для создания)
    id: Optional[str] = Field(None, description="Уникальный идентификатор курса из JSON")
    
    class Config:
        use_enum_values = True
        populate_by_name = True


class TrainingUpdate(BaseModel):
    """Модель для обновления тренировки"""
    activity_type: Optional[str] = Field(None, alias="Activity Type", description="Тип активности")
    program_goal: Optional[List[str]] = Field(None, alias="Program Goal", description="Цели программы")
    training_environment: Optional[List[str]] = Field(None, alias="Training Environment", description="Среда тренировок")
    difficulty_level: Optional[str] = Field(None, alias="Difficulty Level", description="Уровень сложности")
    course_duration_weeks: Optional[int] = Field(None, alias="Course Duration (weeks)", description="Продолжительность курса в неделях")
    weekly_training_frequency: Optional[str] = Field(None, alias="Weekly Training Frequency", description="Частота тренировок в неделю")
    average_workout_duration: Optional[str] = Field(None, alias="Average Workout Duration", description="Средняя продолжительность тренировки")
    age_group: Optional[List[str]] = Field(None, alias="Age Group", description="Возрастная группа")
    gender_orientation: Optional[str] = Field(None, alias="Gender Orientation", description="Гендерная ориентация")
    physical_limitations: Optional[List[str]] = Field(None, alias="Physical Limitations", description="Физические ограничения")
    required_equipment: Optional[List[str]] = Field(None, alias="Required Equipment", description="Необходимое оборудование")
    course_language: Optional[str] = Field(None, alias="Course Language", description="Язык курса")
    visual_content: Optional[List[str]] = Field(None, alias="Visual Content", description="Визуальный контент")
    trainer_feedback_options: Optional[List[str]] = Field(None, alias="Trainer Feedback Options", description="Варианты обратной связи от тренера")
    tags: Optional[List[str]] = Field(None, alias="Tags", description="Теги")
    
    # Данные о тренере
    certification: Optional[Certification] = Field(None, alias="Certification", description="Сертификация тренера")
    experience: Optional[Experience] = Field(None, alias="Experience", description="Опыт тренера")
    trainer_name: Optional[str] = Field(None, alias="Trainer Name", description="Имя тренера")
    
    # Информация о курсе
    course_title: Optional[str] = Field(None, alias="Course Title", description="Название курса")
    program_description: Optional[str] = Field(None, alias="Program Description", description="Описание программы")
    
    # План тренировок
    training_plan: Optional[List[TrainingDay]] = Field(None, alias="training_plan", description="План тренировок")
    
    class Config:
        use_enum_values = True
        populate_by_name = True


class TrainingResponse(BaseModel):
    """Модель для ответа с дополнительными полями"""
    # Основная информация о курсе
    activity_type: str = Field(..., alias="Activity Type", description="Тип активности")
    program_goal: List[str] = Field(..., alias="Program Goal", description="Цели программы")
    training_environment: List[str] = Field(..., alias="Training Environment", description="Среда тренировок")
    difficulty_level: str = Field(..., alias="Difficulty Level", description="Уровень сложности")
    course_duration_weeks: int = Field(..., alias="Course Duration (weeks)", description="Продолжительность курса в неделях")
    weekly_training_frequency: str = Field(..., alias="Weekly Training Frequency", description="Частота тренировок в неделю")
    average_workout_duration: str = Field(..., alias="Average Workout Duration", description="Средняя продолжительность тренировки")
    age_group: List[str] = Field(..., alias="Age Group", description="Возрастная группа")
    gender_orientation: str = Field(..., alias="Gender Orientation", description="Гендерная ориентация")
    physical_limitations: List[str] = Field(..., alias="Physical Limitations", description="Физические ограничения")
    required_equipment: List[str] = Field(..., alias="Required Equipment", description="Необходимое оборудование")
    course_language: str = Field(..., alias="Course Language", description="Язык курса")
    visual_content: List[str] = Field(..., alias="Visual Content", description="Визуальный контент")
    trainer_feedback_options: List[str] = Field(..., alias="Trainer Feedback Options", description="Варианты обратной связи от тренера")
    tags: List[str] = Field(..., alias="Tags", description="Теги")
    
    # Рейтинги и статистика
    average_course_rating: float = Field(..., alias="Average Course Rating", description="Средний рейтинг курса")
    active_participants: int = Field(..., alias="Active Participants", description="Активные участники")
    number_of_reviews: int = Field(..., alias="Number of Reviews", description="Количество отзывов")
    
    # Данные о тренере
    certification: Certification = Field(..., alias="Certification", description="Сертификация тренера")
    experience: Experience = Field(..., alias="Experience", description="Опыт тренера")
    trainer_name: str = Field(..., alias="Trainer Name", description="Имя тренера")
    
    # Информация о курсе
    course_title: str = Field(..., alias="Course Title", description="Название курса")
    program_description: str = Field(..., alias="Program Description", description="Описание программы")
    
    # План тренировок
    training_plan: List[TrainingDay] = Field(..., alias="training_plan", description="План тренировок")
    
    # ID курса
    id: str = Field(..., description="Уникальный идентификатор курса")
    
    # Дополнительные поля для ответа
    db_id: Optional[int] = Field(None, description="ID записи в базе данных")
    user_id: Optional[int] = Field(None, description="ID пользователя")
    created_at: Optional[str] = Field(None, description="Время создания")
    updated_at: Optional[str] = Field(None, description="Время последнего обновления")
    
    class Config:
        use_enum_values = True
        from_attributes = True
        populate_by_name = True


# Deprecated models for backwards compatibility
class Badge(BaseModel):
    """Модель для значков с текстом и цветом"""
    text: str = Field(..., min_length=1, max_length=50, description="Текст значка")
    color: str = Field(..., description="Цвет значка в hex формате")
    
    @validator('text')
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Badge text is required')
        return v.strip()
    
    @validator('color')
    def validate_color(cls, v):
        if not v or not v.strip():
            raise ValueError('Badge color is required')
        
        v = v.strip()
        
        # Проверка hex формата
        hex_pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        if not re.match(hex_pattern, v):
            raise ValueError('Invalid hex color format. Use format #RRGGBB or #RGB')
        
        return v
    
    class Config:
        use_enum_values = True


class HeaderBadges(BaseModel):
    """Модель для значков заголовка (deprecated)"""
    training_type: List[Badge] = Field(..., description="Тип тренировки")
    training_info: List[Badge] = Field(..., description="Информация о тренировке")
    training_equipment: List[Badge] = Field(..., description="Оборудование для тренировки")
    
    class Config:
        use_enum_values = True


class CourseInfo(BaseModel):
    """Модель для информации о курсе (deprecated)"""
    id: str = Field(..., description="ID курса")
    title: str = Field(..., description="Название курса")
    author: str = Field(..., description="Автор курса")
    description: str = Field(..., description="Описание курса")
    rating: float = Field(..., description="Рейтинг курса")
    reviews: int = Field(..., description="Количество отзывов")
    
    class Config:
        use_enum_values = True


class CoachData(BaseModel):
    """Модель для данных тренера (deprecated)"""
    name: str = Field(..., description="Имя тренера")
    profile_picture: Optional[str] = Field(None, description="Ссылка на фото профиля")
    rating: float = Field(..., description="Рейтинг тренера")
    reviews: int = Field(..., description="Количество отзывов")
    years: int = Field(..., description="Количество лет опыта")
    badges: List[Badge] = Field(..., description="Значки тренера")
    
    class Config:
        use_enum_values = True


class TrainingMetadata(BaseModel):
    """Модель для метаданных тренировки (deprecated)"""
    tags: Dict[str, Any] = Field(default_factory=dict, description="Теги")
    certification: Dict[str, Any] = Field(default_factory=dict, description="Сертификация")
    experience: Dict[str, Any] = Field(default_factory=dict, description="Опыт")
    
    class Config:
        use_enum_values = True


# Legacy training model for backwards compatibility
class LegacyTraining(BaseModel):
    """
    Устаревшая модель тренировки для обратной совместимости
    """
    header_badges: HeaderBadges = Field(..., description="Значки заголовка")
    course_info: CourseInfo = Field(..., description="Информация о курсе")
    training_plan: List[TrainingDay] = Field(..., description="План тренировок")
    coach_data: CoachData = Field(..., description="Данные тренера")
    metadata: TrainingMetadata = Field(..., description="Метаданные")
    
    class Config:
        use_enum_values = True


# Alias for backwards compatibility
TrainerCertification = Certification
TrainerExperience = Experience


class TrainerProfile(BaseModel):
    """Модель профиля тренера"""
    profile_picture: Optional[str] = Field(None, max_length=500, description="Ссылка на фото профиля")
    certification: Certification = Field(..., description="Сертификация тренера")
    experience: Experience = Field(..., description="Опыт тренера")
    badges: List[Badge] = Field(default_factory=list, max_items=20, description="Значки тренера (максимум 20)")
    reviews_count: int = Field(0, ge=0, le=100000, description="Количество отзывов")
    bio: Optional[str] = Field(None, min_length=10, max_length=1000, description="Биография тренера")
    
    @validator('profile_picture')
    def validate_profile_picture(cls, v):
        if v is None:
            return v
        
        if not v.strip():
            return None
        
        v = v.strip()
        
        # Проверка URL формата
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, v):
            raise ValueError('Invalid image URL format')
        
        # Проверка поддерживаемых форматов изображений
        supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.gif']
        if not any(v.lower().endswith(fmt) for fmt in supported_formats):
            raise ValueError('Unsupported image format. Supported: jpg, jpeg, png, webp, gif')
        
        if len(v) > 500:
            raise ValueError('URL too long (max 500 characters)')
        
        return v
    
    @validator('badges')
    def validate_badges(cls, v):
        if len(v) > 20:
            raise ValueError('Too many badges (max 20)')
        
        # Проверка на дубликаты значков
        badge_texts = [badge.text.lower() for badge in v]
        if len(badge_texts) != len(set(badge_texts)):
            raise ValueError('Duplicate badges not allowed')
        
        return v
    
    @validator('reviews_count')
    def validate_reviews_count(cls, v):
        if v < 0:
            raise ValueError('Reviews count must be non-negative')
        if v > 100000:
            raise ValueError('Reviews count cannot exceed 100000')
        return v
    
    @validator('bio')
    def validate_bio(cls, v):
        if v is None:
            return v
        
        if not v.strip():
            return None
        
        v = v.strip()
        
        if len(v) < 10:
            raise ValueError('Bio must be at least 10 characters long')
        
        if len(v) > 1000:
            raise ValueError('Bio must be between 10 and 1000 characters')
        
        # Базовая проверка на неприемлемый контент
        inappropriate_words = ['spam', 'fake', 'scam']  # Можно расширить список
        if any(word in v.lower() for word in inappropriate_words):
            raise ValueError('Bio contains inappropriate content')
        
        # Проверка на допустимые символы (буквы, цифры, пунктуация, эмодзи)
        # Разрешаем большинство Unicode символов кроме управляющих
        pattern = r'^[^\x00-\x1f\x7f-\x9f]*$'
        if not re.match(pattern, v):
            raise ValueError('Bio contains invalid characters')
        
        return v
    

    
    class Config:
        use_enum_values = True 