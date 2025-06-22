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


class Training(BaseModel):
    """
    Основная модель тренировки, представляющая полную программу тренировок
    """
    metainfo: str = Field(..., description="Метаинформация о тренировке")
    training_data: TrainingData = Field(..., description="Данные тренировки по дням недели")
    
    # Дополнительные поля для расширенной функциональности
    title: Optional[str] = Field(None, description="Название программы тренировок")
    description: Optional[str] = Field(None, description="Описание программы")
    duration_weeks: Optional[int] = Field(None, description="Продолжительность программы в неделях")
    difficulty_level: Optional[str] = Field(None, description="Уровень сложности")
    created_by: Optional[str] = Field(None, description="Создатель программы")
    
    class Config:
        use_enum_values = True


class TrainingCreate(BaseModel):
    """Модель для создания новой тренировки"""
    metainfo: str = Field(..., description="Метаинформация о тренировке")
    training_data: TrainingData = Field(..., description="Данные тренировки по дням недели")
    title: Optional[str] = Field(None, description="Название программы тренировок")
    description: Optional[str] = Field(None, description="Описание программы")
    duration_weeks: Optional[int] = Field(None, description="Продолжительность программы в неделях")
    difficulty_level: Optional[str] = Field(None, description="Уровень сложности")
    
    class Config:
        use_enum_values = True


class TrainingUpdate(BaseModel):
    """Модель для обновления тренировки - все поля опциональны"""
    metainfo: Optional[str] = Field(None, description="Метаинформация о тренировке")
    training_data: Optional[TrainingData] = Field(None, description="Данные тренировки по дням недели")
    title: Optional[str] = Field(None, description="Название программы тренировок")
    description: Optional[str] = Field(None, description="Описание программы")
    duration_weeks: Optional[int] = Field(None, description="Продолжительность программы в неделях")
    difficulty_level: Optional[str] = Field(None, description="Уровень сложности")
    
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