from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class Badge(BaseModel):
    """Модель для значков с текстом и цветом"""
    text: str = Field(..., description="Текст значка")
    color: str = Field(..., description="Цвет значка в hex формате")
    
    class Config:
        use_enum_values = True


class HeaderBadges(BaseModel):
    """Модель для значков заголовка"""
    training_type: List[Badge] = Field(..., description="Тип тренировки")
    training_info: List[Badge] = Field(..., description="Информация о тренировке")
    training_equipment: List[Badge] = Field(..., description="Оборудование для тренировки")
    
    class Config:
        use_enum_values = True


class CourseInfo(BaseModel):
    """Модель для информации о курсе"""
    id: str = Field(..., description="ID курса")
    title: str = Field(..., description="Название курса")
    author: str = Field(..., description="Автор курса")
    description: str = Field(..., description="Описание курса")
    rating: float = Field(..., description="Рейтинг курса")
    reviews: int = Field(..., description="Количество отзывов")
    
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


class CoachData(BaseModel):
    """Модель для данных тренера"""
    name: str = Field(..., description="Имя тренера")
    profile_picture: Optional[str] = Field(None, description="Ссылка на фото профиля")
    rating: float = Field(..., description="Рейтинг тренера")
    reviews: int = Field(..., description="Количество отзывов")
    years: int = Field(..., description="Количество лет опыта")
    badges: List[Badge] = Field(..., description="Значки тренера")
    
    class Config:
        use_enum_values = True


class TrainingMetadata(BaseModel):
    """Модель для метаданных тренировки"""
    tags: Dict[str, Any] = Field(default_factory=dict, description="Теги")
    certification: Dict[str, Any] = Field(default_factory=dict, description="Сертификация")
    experience: Dict[str, Any] = Field(default_factory=dict, description="Опыт")
    
    class Config:
        use_enum_values = True


class Training(BaseModel):
    """
    Основная модель тренировки, представляющая полную программу тренировок
    """
    header_badges: HeaderBadges = Field(..., description="Значки заголовка")
    course_info: CourseInfo = Field(..., description="Информация о курсе")
    training_plan: List[TrainingDay] = Field(..., description="План тренировок")
    coach_data: CoachData = Field(..., description="Данные тренера")
    metadata: TrainingMetadata = Field(..., description="Метаданные")
    
    class Config:
        use_enum_values = True


class CourseInfoCreate(BaseModel):
    """Модель для создания информации о курсе - автор заполняется автоматически"""
    id: str = Field(..., description="ID курса")
    title: str = Field(..., description="Название курса")
    # author заполняется автоматически на сервере из имени пользователя
    description: str = Field(..., description="Описание курса")
    # rating и reviews заполняются автоматически из профиля тренера, если не указаны
    rating: Optional[float] = Field(None, description="Рейтинг курса (автоматически из профиля тренера, если не указан)")
    reviews: Optional[int] = Field(None, description="Количество отзывов (автоматически из профиля тренера, если не указано)")
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "id": "course_001",
                "title": "Complete Beginner Workout",
                "description": "A comprehensive workout program for beginners"
                # author, rating, reviews will be auto-filled from trainer profile
            }
        }


class CoachDataCreate(BaseModel):
    """Модель для создания данных тренера - все поля заполняются автоматически"""
    # Все поля (name, profile_picture, rating, reviews, years, badges) заполняются автоматически на сервере
    pass
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {}
            # Все поля заполняются автоматически из trainer_profile
        }


class TrainingCreateMinimal(BaseModel):
    """
    Модель для создания новой тренировки с минимальными данными.
    
    АВТОМАТИЧЕСКИ ЗАПОЛНЯЕТСЯ НА СЕРВЕРЕ:
    - coach_data.name, profile_picture, rating, reviews, years из профиля тренера
    - course_info.author из имени пользователя
    - course_info.rating и reviews из профиля тренера (если не указаны)
    """
    header_badges: HeaderBadges = Field(..., description="Значки заголовка")
    course_info: CourseInfoCreate = Field(
        ..., 
        description="Информация о курсе (автор заполняется автоматически)"
    )
    training_plan: List[TrainingDay] = Field(..., description="План тренировок")
    coach_data: Optional[CoachDataCreate] = Field(
        default_factory=CoachDataCreate, 
        description="Дополнительные данные тренера (основные поля заполняются автоматически)"
    )
    metadata: Optional[TrainingMetadata] = Field(default_factory=TrainingMetadata, description="Метаданные")
    
    class Config:
        use_enum_values = True
        schema_extra = {
            "example": {
                "header_badges": {
                    "training_type": [{"text": "Strength", "color": "#FF6B6B"}],
                    "training_info": [{"text": "Beginner", "color": "#4ECDC4"}],
                    "training_equipment": [{"text": "No Equipment", "color": "#45B7D1"}]
                },
                "course_info": {
                    "id": "course_001",
                    "title": "Complete Beginner Workout",
                    "description": "A comprehensive workout program for beginners"
                    # author, rating, reviews will be filled automatically
                },
                "training_plan": [
                    {
                        "title": "Day 1: Upper Body",
                        "exercises": [
                            {
                                "exercise": "Push-ups",
                                "repeats": "10-15",
                                "sets": "3",
                                "duration": "30 seconds",
                                "rest": "60 seconds",
                                "description": "Standard push-ups focusing on chest and arms"
                            }
                        ]
                    }
                ],
                "coach_data": {}
            }
        }


class TrainingCreate(BaseModel):
    """Модель для создания новой тренировки"""
    header_badges: HeaderBadges = Field(..., description="Значки заголовка")
    course_info: CourseInfo = Field(..., description="Информация о курсе")
    training_plan: List[TrainingDay] = Field(..., description="План тренировок")
    coach_data: CoachData = Field(..., description="Данные тренера")
    metadata: Optional[TrainingMetadata] = Field(default_factory=TrainingMetadata, description="Метаданные")
    
    class Config:
        use_enum_values = True


class TrainingUpdate(BaseModel):
    """Модель для обновления тренировки - все поля опциональны"""
    header_badges: Optional[HeaderBadges] = Field(None, description="Значки заголовка")
    course_info: Optional[CourseInfo] = Field(None, description="Информация о курсе")
    training_plan: Optional[List[TrainingDay]] = Field(None, description="План тренировок")
    coach_data: Optional[CoachData] = Field(None, description="Данные тренера")
    metadata: Optional[TrainingMetadata] = Field(None, description="Метаданные")
    
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


# Дополнительные модели для работы с тренерами
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
    profile_picture: Optional[str] = Field(None, description="Ссылка на фото профиля")
    certification: TrainerCertification = Field(..., description="Сертификация тренера")
    experience: TrainerExperience = Field(..., description="Опыт тренера")
    badges: List[Badge] = Field(default_factory=list, description="Значки тренера")
    reviews_count: int = Field(0, description="Количество отзывов")
    bio: Optional[str] = Field(None, description="Биография тренера")
    
    class Config:
        use_enum_values = True 