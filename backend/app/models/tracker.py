from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ScheduleInstance(BaseModel):
    """
    Модель для одного элемента расписания
    """
    date: str = Field(..., description="Дата в формате ДД.ММ.ГГГГ", example="21.07.2025")
    index: int = Field(..., ge=0, description="Номер тренировки в training_plan (начиная с 0)")
    course_id: str = Field(..., description="ID тренировочного плана")


class AddScheduleRequest(BaseModel):
    """
    Запрос на добавление расписания
    """
    schedule: List[ScheduleInstance] = Field(..., description="Список элементов расписания")


class ScheduleResponse(BaseModel):
    """
    Ответ с расписанием пользователя
    """
    user_id: int = Field(..., description="ID пользователя")
    total_instances: int = Field(..., description="Общее количество элементов расписания")
    schedule: List[ScheduleInstance] = Field(..., description="Список элементов расписания")


class TrainingDayInfo(BaseModel):
    """
    Информация о дне тренировки из training_plan
    """
    course_id: str = Field(..., description="ID курса")
    course_title: str = Field(..., description="Название курса")
    training_index: int = Field(..., description="Номер тренировки в плане")
    training_day: Dict[str, Any] = Field(..., description="Полная информация о тренировочном дне")


class TrainingByDateResponse(BaseModel):
    """
    Ответ с тренировками на конкретную дату
    """
    date: str = Field(..., description="Дата в формате ДД.ММ.ГГГГ")
    trainings: List[TrainingDayInfo] = Field(..., description="Список тренировок на эту дату")


class AddScheduleResponse(BaseModel):
    """
    Ответ на добавление расписания
    """
    message: str = Field(..., description="Сообщение о результате")
    added_instances: int = Field(..., description="Количество добавленных элементов")
    user_id: int = Field(..., description="ID пользователя")


class DeleteScheduleResponse(BaseModel):
    """
    Ответ на удаление расписания
    """
    message: str = Field(..., description="Сообщение о результате")
    deleted_instances: int = Field(..., description="Количество удаленных элементов") 