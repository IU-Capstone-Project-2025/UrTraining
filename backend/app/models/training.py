from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class DayOfWeek(str, Enum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Exercise(BaseModel):
    """Модель для отдельного упражнения в тренировке"""
    exercise_name: str = Field(..., description="Название упражнения")
    repetitions: Optional[str] = Field(None, description="Количество повторений")
    sets: Optional[str] = Field(None, description="Количество подходов")
    weight: Optional[str] = Field(None, description="Вес (кг)")
    duration: Optional[str] = Field(None, description="Продолжительность (мин:сек)")
    rest_time: Optional[str] = Field(None, description="Время отдыха между подходами")
    notes: Optional[str] = Field(None, description="Дополнительные заметки")
    
    class Config:
        use_enum_values = True


class DayTraining(BaseModel):
    """Модель для тренировки одного дня"""
    exercises: List[Exercise] = Field(..., description="Список упражнений на день")
    
    class Config:
        use_enum_values = True


class TrainingData(BaseModel):
    """Модель для данных тренировки по дням недели"""
    monday: Optional[List[Exercise]] = Field(None, description="Упражнения на понедельник")
    tuesday: Optional[List[Exercise]] = Field(None, description="Упражнения на вторник")
    wednesday: Optional[List[Exercise]] = Field(None, description="Упражнения на среду")
    thursday: Optional[List[Exercise]] = Field(None, description="Упражнения на четверг")
    friday: Optional[List[Exercise]] = Field(None, description="Упражнения на пятницу")
    saturday: Optional[List[Exercise]] = Field(None, description="Упражнения на субботу")
    sunday: Optional[List[Exercise]] = Field(None, description="Упражнения на воскресенье")
    
    class Config:
        use_enum_values = True


class TrainerCertification(BaseModel):
    """Модель для сертификации тренера"""
    type: str = Field(..., description="Тип сертификации (ISSA, ACE, NASM и т.д.)")
    level: str = Field(..., description="Уровень сертификации (Basic, Advanced, Master)")
    specialization: str = Field(..., description="Специализация")
    
    class Config:
        use_enum_values = True


class TrainerExperience(BaseModel):
    """Модель для опыта тренера"""
    years: int = Field(..., description="Количество лет опыта")
    specialization: str = Field(..., description="Специализация")
    courses: int = Field(..., description="Количество созданных курсов")
    rating: float = Field(..., description="Рейтинг тренера")
    
    class Config:
        use_enum_values = True


class TrainerProfile(BaseModel):
    """Модель профиля тренера"""
    name: str = Field(..., description="Имя тренера")
    certification: TrainerCertification = Field(..., description="Сертификация тренера")
    experience: TrainerExperience = Field(..., description="Опыт тренера")
    
    class Config:
        use_enum_values = True


class TrainingMetadata(BaseModel):
    """Модель для метаданных тренировки"""
    # Основные характеристики тренировки
    activity_type: str = Field(default="General Training", description="Тип активности")
    program_goal: List[str] = Field(default=["Maintain Fitness"], description="Цели программы")
    training_environment: List[str] = Field(default=["Universal"], description="Среда тренировок")
    difficulty_level: str = Field(default="Beginner", description="Уровень сложности")
    course_duration_weeks: int = Field(default=1, description="Продолжительность курса в неделях")
    weekly_training_frequency: str = Field(default="3-4 times", description="Частота тренировок в неделю")
    average_workout_duration: str = Field(default="30-45 minutes", description="Средняя продолжительность тренировки")
    age_group: List[str] = Field(default=["All Ages"], description="Возрастная группа")
    gender_orientation: str = Field(default="Unisex", description="Гендерная ориентация")
    physical_limitations: List[str] = Field(default=[], description="Физические ограничения")
    required_equipment: List[str] = Field(default=["No Equipment"], description="Необходимое оборудование")
    course_language: str = Field(default="English", description="Язык курса")
    visual_content: List[str] = Field(default=["Minimal Visual Content"], description="Визуальный контент")
    trainer_feedback_options: List[str] = Field(default=[], description="Опции обратной связи с тренером")
    tags: List[str] = Field(default=[], description="Теги")
    
    # Статистика курса
    average_course_rating: float = Field(default=0.0, description="Средний рейтинг курса")
    active_participants: int = Field(default=0, description="Активные участники")
    number_of_reviews: int = Field(default=0, description="Количество отзывов")
    
    # Информация о тренере (может быть заполнена из trainer_profile пользователя)
    trainer_name: Optional[str] = Field(default=None, description="Имя тренера")
    certification: Optional[TrainerCertification] = Field(default=None, description="Сертификация тренера")
    experience: Optional[TrainerExperience] = Field(default=None, description="Опыт тренера")
    
    class Config:
        use_enum_values = True


class Training(BaseModel):
    """
    Основная модель тренировки, представляющая полную программу тренировок
    """
    metadata: TrainingMetadata = Field(..., description="Метаданные о тренировке")
    training_data: TrainingData = Field(..., description="Данные тренировки по дням недели")
    
    # Дополнительные поля для расширенной функциональности
    title: Optional[str] = Field(None, description="Название программы тренировок")
    description: Optional[str] = Field(None, description="Описание программы")
    
    class Config:
        use_enum_values = True


class TrainingCreate(BaseModel):
    """Модель для создания новой тренировки"""
    metadata: TrainingMetadata = Field(..., description="Метаданные о тренировке")
    training_data: TrainingData = Field(..., description="Данные тренировки по дням недели")
    title: Optional[str] = Field(None, description="Название программы тренировок")
    description: Optional[str] = Field(None, description="Описание программы")
    
    class Config:
        use_enum_values = True


class TrainingUpdate(BaseModel):
    """Модель для обновления тренировки - все поля опциональны"""
    metadata: Optional[TrainingMetadata] = Field(None, description="Метаданные о тренировке")
    training_data: Optional[TrainingData] = Field(None, description="Данные тренировки по дням недели")
    title: Optional[str] = Field(None, description="Название программы тренировок")
    description: Optional[str] = Field(None, description="Описание программы")
    
    class Config:
        use_enum_values = True


class TrainingResponse(Training):
    """Модель для ответа с дополнительными полями"""
    id: Optional[int] = Field(None, description="ID тренировки")
    user_id: Optional[int] = Field(None, description="ID пользователя")
    created_at: Optional[str] = Field(None, description="Время создания")
    updated_at: Optional[str] = Field(None, description="Время последнего обновления")
    
    class Config:
        use_enum_values = True
        from_attributes = True 