from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from enum import Enum


class Certification(BaseModel):
    """Модель для сертификации тренера"""
    Type: str = Field(..., description="Тип сертификации (ISSA, ACE, NASM и т.д.)")
    Level: str = Field(..., description="Уровень сертификации (Basic, Advanced, Master)")
    Specialization: str = Field(..., description="Специализация")
    
    class Config:
        use_enum_values = True


class Experience(BaseModel):
    """Модель для опыта тренера"""
    Years: int = Field(..., description="Количество лет опыта")
    Specialization: str = Field(..., description="Специализация")
    Courses: int = Field(..., description="Количество созданных курсов")
    Rating: float = Field(..., description="Рейтинг тренера")
    
    class Config:
        use_enum_values = True


class Exercise(BaseModel):
    """Модель для упражнения"""
    exercise: str = Field(..., description="Название упражнения")
    repeats: str = Field(..., description="Количество повторений")
    sets: str = Field(..., description="Количество подходов")
    duration: str = Field(..., description="Продолжительность")
    rest: str = Field(..., description="Время отдыха")
    description: str = Field(..., description="Описание упражнения")
    
    class Config:
        use_enum_values = True


class TrainingDay(BaseModel):
    """Модель для тренировочного дня"""
    title: str = Field(..., description="Название дня тренировки")
    exercises: List[Exercise] = Field(..., description="Список упражнений")
    
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
    activity_type: str = Field(..., description="Тип активности")
    program_goal: List[str] = Field(..., description="Цели программы")
    training_environment: List[str] = Field(..., description="Среда тренировок")
    difficulty_level: str = Field(..., description="Уровень сложности")
    course_duration_weeks: int = Field(..., description="Продолжительность курса в неделях")
    weekly_training_frequency: str = Field(..., description="Частота тренировок в неделю")
    average_workout_duration: str = Field(..., description="Средняя продолжительность тренировки")
    age_group: List[str] = Field(..., description="Возрастная группа")
    gender_orientation: str = Field(..., description="Гендерная ориентация")
    physical_limitations: List[str] = Field(default_factory=list, description="Физические ограничения")
    required_equipment: List[str] = Field(..., description="Необходимое оборудование")
    course_language: str = Field(..., description="Язык курса")
    visual_content: List[str] = Field(..., description="Визуальный контент")
    trainer_feedback_options: List[str] = Field(..., description="Варианты обратной связи от тренера")
    tags: List[str] = Field(default_factory=list, description="Теги")
    
    # Данные о тренере
    certification: Certification = Field(..., description="Сертификация тренера")
    experience: Experience = Field(..., description="Опыт тренера")
    trainer_name: str = Field(..., description="Имя тренера")
    
    # Информация о курсе
    course_title: str = Field(..., description="Название курса")
    program_description: str = Field(..., description="Описание программы")
    
    # План тренировок
    training_plan: List[TrainingDay] = Field(..., description="План тренировок")
    
    class Config:
        use_enum_values = True


class TrainingUpdate(BaseModel):
    """Модель для обновления тренировки"""
    activity_type: Optional[str] = Field(None, description="Тип активности")
    program_goal: Optional[List[str]] = Field(None, description="Цели программы")
    training_environment: Optional[List[str]] = Field(None, description="Среда тренировок")
    difficulty_level: Optional[str] = Field(None, description="Уровень сложности")
    course_duration_weeks: Optional[int] = Field(None, description="Продолжительность курса в неделях")
    weekly_training_frequency: Optional[str] = Field(None, description="Частота тренировок в неделю")
    average_workout_duration: Optional[str] = Field(None, description="Средняя продолжительность тренировки")
    age_group: Optional[List[str]] = Field(None, description="Возрастная группа")
    gender_orientation: Optional[str] = Field(None, description="Гендерная ориентация")
    physical_limitations: Optional[List[str]] = Field(None, description="Физические ограничения")
    required_equipment: Optional[List[str]] = Field(None, description="Необходимое оборудование")
    course_language: Optional[str] = Field(None, description="Язык курса")
    visual_content: Optional[List[str]] = Field(None, description="Визуальный контент")
    trainer_feedback_options: Optional[List[str]] = Field(None, description="Варианты обратной связи от тренера")
    tags: Optional[List[str]] = Field(None, description="Теги")
    
    # Данные о тренере
    certification: Optional[Certification] = Field(None, description="Сертификация тренера")
    experience: Optional[Experience] = Field(None, description="Опыт тренера")
    trainer_name: Optional[str] = Field(None, description="Имя тренера")
    
    # Информация о курсе
    course_title: Optional[str] = Field(None, description="Название курса")
    program_description: Optional[str] = Field(None, description="Описание программы")
    
    # План тренировок
    training_plan: Optional[List[TrainingDay]] = Field(None, description="План тренировок")
    
    class Config:
        use_enum_values = True


class TrainingResponse(BaseModel):
    """Модель для ответа с дополнительными полями"""
    # Основная информация о курсе
    activity_type: str = Field(..., description="Тип активности")
    program_goal: List[str] = Field(..., description="Цели программы")
    training_environment: List[str] = Field(..., description="Среда тренировок")
    difficulty_level: str = Field(..., description="Уровень сложности")
    course_duration_weeks: int = Field(..., description="Продолжительность курса в неделях")
    weekly_training_frequency: str = Field(..., description="Частота тренировок в неделю")
    average_workout_duration: str = Field(..., description="Средняя продолжительность тренировки")
    age_group: List[str] = Field(..., description="Возрастная группа")
    gender_orientation: str = Field(..., description="Гендерная ориентация")
    physical_limitations: List[str] = Field(..., description="Физические ограничения")
    required_equipment: List[str] = Field(..., description="Необходимое оборудование")
    course_language: str = Field(..., description="Язык курса")
    visual_content: List[str] = Field(..., description="Визуальный контент")
    trainer_feedback_options: List[str] = Field(..., description="Варианты обратной связи от тренера")
    tags: List[str] = Field(..., description="Теги")
    
    # Рейтинги и статистика
    average_course_rating: float = Field(..., description="Средний рейтинг курса")
    active_participants: int = Field(..., description="Активные участники")
    number_of_reviews: int = Field(..., description="Количество отзывов")
    
    # Данные о тренере
    certification: Certification = Field(..., description="Сертификация тренера")
    experience: Experience = Field(..., description="Опыт тренера")
    trainer_name: str = Field(..., description="Имя тренера")
    
    # Информация о курсе
    course_title: str = Field(..., description="Название курса")
    program_description: str = Field(..., description="Описание программы")
    
    # План тренировок
    training_plan: List[TrainingDay] = Field(..., description="План тренировок")
    
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


# Deprecated models for backwards compatibility
class Badge(BaseModel):
    """Модель для значков с текстом и цветом (deprecated)"""
    text: str = Field(..., description="Текст значка")
    color: str = Field(..., description="Цвет значка в hex формате")
    
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
    profile_picture: Optional[str] = Field(None, description="Ссылка на фото профиля")
    certification: Certification = Field(..., description="Сертификация тренера")
    experience: Experience = Field(..., description="Опыт тренера")
    badges: List[Badge] = Field(default_factory=list, description="Значки тренера")
    reviews_count: int = Field(0, description="Количество отзывов")
    bio: Optional[str] = Field(None, description="Биография тренера")
    
    class Config:
        use_enum_values = True 