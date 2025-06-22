from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.crud import (
    get_training_by_id, 
    get_trainings_summary, 
    get_trainings_by_user,
    create_training,
    update_training,
    delete_training,
    search_trainings
)
from app.models.training import (
    TrainingResponse, 
    TrainingCreate, 
    TrainingUpdate
)
from app.routes.auth import get_current_user

router = APIRouter()


# Pydantic модель для краткой информации о тренировке (для каталога)
class TrainingSummary(BaseModel):
    id: int
    title: Optional[str] = None
    metainfo: str
    description: Optional[str] = None
    difficulty_level: Optional[str] = None
    duration_weeks: Optional[int] = None
    created_by: Optional[str] = None
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TrainingSummary])
async def get_trainings_catalog(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество записей"),
    search: Optional[str] = Query(None, description="Поиск по названию или описанию"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех тренировочных программ с краткой информацией.
    
    Этот эндпоинт используется для отображения каталога тренировок.
    Возвращает только основную информацию: название, метадату, описание и базовые характеристики.
    """
    try:
        if search:
            trainings = search_trainings(db, search, skip, limit)
        else:
            trainings = get_trainings_summary(db, skip, limit)
        
        # Преобразуем в формат для краткого отображения
        training_summaries = []
        for training in trainings:
            training_summaries.append(TrainingSummary(
                id=training.id,
                title=training.title,
                metainfo=training.metainfo,
                description=training.description,
                difficulty_level=training.difficulty_level,
                duration_weeks=training.duration_weeks,
                created_by=training.created_by,
                created_at=training.created_at.isoformat() if training.created_at else None
            ))
        
        return training_summaries
        
    except Exception as e:
        print(f"Error fetching trainings catalog: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить каталог тренировок"
        )


@router.get("/{training_id}", response_model=TrainingResponse)
async def get_training_details(
    training_id: int,
    db: Session = Depends(get_db)
):
    """
    Получить полную информацию о конкретной тренировочной программе.
    
    Этот эндпоинт используется для детального просмотра тренировки.
    Возвращает всю информацию включая данные упражнений по дням недели.
    """
    try:
        training = get_training_by_id(db, training_id)
        
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Преобразуем SQLAlchemy объект в Pydantic модель
        training_response = TrainingResponse(
            id=training.id,
            user_id=training.user_id,
            metainfo=training.metainfo,
            training_data=training.training_data,
            title=training.title,
            description=training.description,
            duration_weeks=training.duration_weeks,
            difficulty_level=training.difficulty_level,
            created_by=training.created_by,
            created_at=training.created_at.isoformat() if training.created_at else None,
            updated_at=training.updated_at.isoformat() if training.updated_at else None
        )
        
        return training_response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching training details: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить детали тренировки"
        )


@router.post("/", response_model=TrainingResponse)
async def create_training_program(
    training_data: TrainingCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создать новую тренировочную программу.
    
    Требует авторизации. Созданная программа будет привязана к текущему пользователю.
    """
    try:
        # Преобразуем Pydantic модель в словарь
        training_dict = training_data.model_dump()
        
        # Добавляем информацию о создателе
        training_dict["created_by"] = current_user["username"]
        
        # Создаем тренировку
        db_training = create_training(db, training_dict, current_user["id"])
        
        # Возвращаем созданную тренировку
        return TrainingResponse(
            id=db_training.id,
            user_id=db_training.user_id,
            metainfo=db_training.metainfo,
            training_data=db_training.training_data,
            title=db_training.title,
            description=db_training.description,
            duration_weeks=db_training.duration_weeks,
            difficulty_level=db_training.difficulty_level,
            created_by=db_training.created_by,
            created_at=db_training.created_at.isoformat() if db_training.created_at else None,
            updated_at=db_training.updated_at.isoformat() if db_training.updated_at else None
        )
        
    except Exception as e:
        print(f"Error creating training: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось создать тренировочную программу"
        )


@router.put("/{training_id}", response_model=TrainingResponse)
async def update_training_program(
    training_id: int,
    training_data: TrainingUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить существующую тренировочную программу.
    
    Требует авторизации. Пользователь может редактировать только свои тренировки.
    """
    try:
        # Проверяем существование тренировки
        existing_training = get_training_by_id(db, training_id)
        if not existing_training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Проверяем права на редактирование
        if existing_training.user_id != current_user["id"] and not current_user.get("is_admin", False):
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав для редактирования этой тренировки"
            )
        
        # Обновляем тренировку
        training_dict = training_data.model_dump(exclude_unset=True)
        updated_training = update_training(db, training_id, training_dict)
        
        if not updated_training:
            raise HTTPException(
                status_code=500,
                detail="Не удалось обновить тренировку"
            )
        
        return TrainingResponse(
            id=updated_training.id,
            user_id=updated_training.user_id,
            metainfo=updated_training.metainfo,
            training_data=updated_training.training_data,
            title=updated_training.title,
            description=updated_training.description,
            duration_weeks=updated_training.duration_weeks,
            difficulty_level=updated_training.difficulty_level,
            created_by=updated_training.created_by,
            created_at=updated_training.created_at.isoformat() if updated_training.created_at else None,
            updated_at=updated_training.updated_at.isoformat() if updated_training.updated_at else None
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating training: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось обновить тренировочную программу"
        )


@router.delete("/{training_id}")
async def delete_training_program(
    training_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить тренировочную программу.
    
    Требует авторизации. Пользователь может удалять только свои тренировки.
    Выполняется мягкое удаление (деактивация).
    """
    try:
        # Проверяем существование тренировки
        existing_training = get_training_by_id(db, training_id)
        if not existing_training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Проверяем права на удаление
        if existing_training.user_id != current_user["id"] and not current_user.get("is_admin", False):
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав для удаления этой тренировки"
            )
        
        # Удаляем тренировку
        success = delete_training(db, training_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Не удалось удалить тренировку"
            )
        
        return {"message": "Тренировочная программа успешно удалена"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting training: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось удалить тренировочную программу"
        )


@router.get("/user/my", response_model=List[TrainingSummary])
async def get_my_trainings(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество записей"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить список тренировочных программ текущего пользователя.
    
    Требует авторизации.
    """
    try:
        trainings = get_trainings_by_user(db, current_user["id"], skip, limit)
        
        # Преобразуем в формат для краткого отображения
        training_summaries = []
        for training in trainings:
            training_summaries.append(TrainingSummary(
                id=training.id,
                title=training.title,
                metainfo=training.metainfo,
                description=training.description,
                difficulty_level=training.difficulty_level,
                duration_weeks=training.duration_weeks,
                created_by=training.created_by,
                created_at=training.created_at.isoformat() if training.created_at else None
            ))
        
        return training_summaries
        
    except Exception as e:
        print(f"Error fetching user trainings: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить ваши тренировки"
        ) 