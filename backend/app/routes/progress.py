from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from app.database import get_db
from app.crud import (
    update_training_progress,
    get_training_progress_by_course_id,
    get_user_training_progresses,
    reset_training_progress,
    get_training_by_course_id
)
from app.routes.auth import get_current_user

router = APIRouter()

# Pydantic models
class UpdateProgressRequest(BaseModel):
    course_id: str = Field(..., description="ID курса тренировки")
    item_number: int = Field(..., ge=0, description="Номер выполненного item (начиная с 0)")

class ProgressResponse(BaseModel):
    course_id: str
    total_items: int
    completed_items: List[int]
    progress_percentage: float
    last_completed_item: Optional[int]
    started_at: str
    last_updated: str

class UpdateProgressResponse(BaseModel):
    message: str
    progress: ProgressResponse

class ResetProgressRequest(BaseModel):
    course_id: str = Field(..., description="ID курса тренировки")

@router.post("/update", response_model=UpdateProgressResponse)
async def update_progress(
    request: UpdateProgressRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить прогресс пользователя - отметить item как выполненный
    """
    try:
        # Найти тренировку по course_id
        training = get_training_by_course_id(db, request.course_id)
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировка с ID {request.course_id} не найдена"
            )
        
        # Обновить прогресс
        progress = update_training_progress(
            db, 
            current_user["id"], 
            training.id, 
            request.item_number
        )
        
        progress_response = ProgressResponse(
            course_id=request.course_id,
            total_items=progress.total_items,
            completed_items=progress.completed_items,
            progress_percentage=progress.progress_percentage,
            last_completed_item=progress.last_completed_item,
            started_at=progress.started_at.isoformat(),
            last_updated=progress.last_updated.isoformat()
        )
        
        return UpdateProgressResponse(
            message=f"Item {request.item_number} отмечен как выполненный. Прогресс: {progress.progress_percentage:.1f}%",
            progress=progress_response
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error updating progress: {e}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )


@router.get("/{course_id}", response_model=ProgressResponse)
async def get_progress(
    course_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить прогресс пользователя по конкретной тренировке
    """
    try:
        progress = get_training_progress_by_course_id(db, current_user["id"], course_id)
        
        if not progress:
            # Если прогресса нет, проверяем существует ли тренировка
            training = get_training_by_course_id(db, course_id)
            if not training:
                raise HTTPException(
                    status_code=404,
                    detail=f"Тренировка с ID {course_id} не найдена"
                )
            
            # Возвращаем пустой прогресс
            total_items = len(training.training_plan) if training.training_plan else 0
            return ProgressResponse(
                course_id=course_id,
                total_items=total_items,
                completed_items=[],
                progress_percentage=0.0,
                last_completed_item=None,
                started_at="",
                last_updated=""
            )
        
        return ProgressResponse(
            course_id=course_id,
            total_items=progress.total_items,
            completed_items=progress.completed_items,
            progress_percentage=progress.progress_percentage,
            last_completed_item=progress.last_completed_item,
            started_at=progress.started_at.isoformat(),
            last_updated=progress.last_updated.isoformat()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting progress: {e}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )


@router.get("/", response_model=List[ProgressResponse])
async def get_all_progress(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить весь прогресс пользователя по всем тренировкам
    """
    try:
        progresses = get_user_training_progresses(db, current_user["id"], skip, limit)
        
        result = []
        for progress in progresses:
            # Получить course_id из связанной тренировки
            training = progress.training
            if training:
                progress_response = ProgressResponse(
                    course_id=training.course_id,
                    total_items=progress.total_items,
                    completed_items=progress.completed_items,
                    progress_percentage=progress.progress_percentage,
                    last_completed_item=progress.last_completed_item,
                    started_at=progress.started_at.isoformat(),
                    last_updated=progress.last_updated.isoformat()
                )
                result.append(progress_response)
        
        return result
        
    except Exception as e:
        print(f"Error getting all progress: {e}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )


@router.post("/reset", response_model=dict)
async def reset_progress(
    request: ResetProgressRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Сбросить прогресс пользователя по тренировке
    """
    try:
        # Найти тренировку по course_id
        training = get_training_by_course_id(db, request.course_id)
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировка с ID {request.course_id} не найдена"
            )
        
        success = reset_training_progress(db, current_user["id"], training.id)
        
        if success:
            return {"message": "Прогресс успешно сброшен"}
        else:
            return {"message": "Прогресс не найден или уже был пустым"}
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error resetting progress: {e}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        ) 