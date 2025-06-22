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
    search_trainings,
    get_training_with_trainer_info,
    get_user_by_id
)
from app.models.training import (
    TrainingResponse, 
    TrainingCreate, 
    TrainingUpdate,
    TrainingMetadata
)
from app.routes.auth import get_current_user

router = APIRouter()


# Pydantic модель для краткой информации о тренировке (для каталога)
class TrainingSummary(BaseModel):
    id: int
    title: Optional[str] = None
    metadata: Optional[TrainingMetadata] = None
    description: Optional[str] = None
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
            # Обрабатываем случай когда training_metadata может быть None или пустым
            metadata = training.training_metadata or {}
            try:
                # Пытаемся создать TrainingMetadata объект, используя дефолтные значения
                training_metadata = TrainingMetadata(**metadata)
            except Exception as e:
                print(f"Error parsing metadata for training {training.id}: {e}")
                # Создаем объект с дефолтными значениями
                training_metadata = TrainingMetadata()
            
            training_summaries.append(TrainingSummary(
                id=training.id,
                title=training.title,
                metadata=training_metadata,
                description=training.description,
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
        # Используем новую функцию для получения тренировки с информацией о тренере
        training = get_training_with_trainer_info(db, training_id)
        
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Обрабатываем метаданные
        metadata = training.training_metadata or {}
        try:
            training_metadata = TrainingMetadata(**metadata)
        except Exception as e:
            print(f"Error parsing metadata for training {training.id}: {e}")
            training_metadata = TrainingMetadata()
        
        # Преобразуем SQLAlchemy объект в Pydantic модель
        training_response = TrainingResponse(
            id=training.id,
            user_id=training.user_id,
            metadata=training_metadata,
            training_data=training.training_data,
            title=training.title,
            description=training.description,
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
    
    Требует авторизации и наличия профиля тренера. 
    Созданная программа будет привязана к текущему пользователю.
    """
    try:
        # Проверяем наличие профиля тренера у пользователя
        user = get_user_by_id(db, current_user["id"])
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден"
            )
        
        if not user.trainer_profile:
            raise HTTPException(
                status_code=403,
                detail="Для создания тренировочных программ необходимо настроить профиль тренера. Пожалуйста, заполните информацию о ваших сертификатах и опыте работы."
            )
        
        # Преобразуем Pydantic модель в словарь
        training_dict = training_data.model_dump()
        
        # Создаем тренировку
        db_training = create_training(db, training_dict, current_user["id"])
        
        # Обрабатываем метаданные для ответа
        metadata = db_training.training_metadata or {}
        try:
            training_metadata = TrainingMetadata(**metadata)
        except Exception as e:
            print(f"Error parsing metadata for new training: {e}")
            training_metadata = TrainingMetadata()
        
        # Возвращаем созданную тренировку
        return TrainingResponse(
            id=db_training.id,
            user_id=db_training.user_id,
            metadata=training_metadata,
            training_data=db_training.training_data,
            title=db_training.title,
            description=db_training.description,
            created_at=db_training.created_at.isoformat() if db_training.created_at else None,
            updated_at=db_training.updated_at.isoformat() if db_training.updated_at else None
        )
        
    except HTTPException:
        raise
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
    
    Требует авторизации и наличия профиля тренера.
    Пользователь может редактировать только свои тренировки.
    """
    try:
        # Проверяем наличие профиля тренера у пользователя
        user = get_user_by_id(db, current_user["id"])
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден"
            )
        
        if not user.trainer_profile and not current_user.get("is_admin", False):
            raise HTTPException(
                status_code=403,
                detail="Для редактирования тренировочных программ необходимо иметь профиль тренера"
            )
        
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
        
        # Обрабатываем метаданные для ответа
        metadata = updated_training.training_metadata or {}
        try:
            training_metadata = TrainingMetadata(**metadata)
        except Exception as e:
            print(f"Error parsing metadata for updated training: {e}")
            training_metadata = TrainingMetadata()
        
        return TrainingResponse(
            id=updated_training.id,
            user_id=updated_training.user_id,
            metadata=training_metadata,
            training_data=updated_training.training_data,
            title=updated_training.title,
            description=updated_training.description,
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
            # Обрабатываем случай когда training_metadata может быть None или пустым
            metadata = training.training_metadata or {}
            try:
                training_metadata = TrainingMetadata(**metadata)
            except Exception as e:
                print(f"Error parsing metadata for user training {training.id}: {e}")
                training_metadata = TrainingMetadata()
            
            training_summaries.append(TrainingSummary(
                id=training.id,
                title=training.title,
                metadata=training_metadata,
                description=training.description,
                created_at=training.created_at.isoformat() if training.created_at else None
            ))
        
        return training_summaries
        
    except Exception as e:
        print(f"Error fetching user trainings: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить ваши тренировки"
        )


@router.get("/can-create", response_model=dict)
async def can_create_training(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Проверить, может ли текущий пользователь создавать тренировочные программы.
    
    Требует авторизации.
    """
    try:
        # Проверяем наличие профиля тренера у пользователя
        user = get_user_by_id(db, current_user["id"])
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден"
            )
        
        can_create = bool(user.trainer_profile) or current_user.get("is_admin", False)
        
        response = {
            "can_create": can_create,
            "has_trainer_profile": bool(user.trainer_profile),
            "is_admin": current_user.get("is_admin", False)
        }
        
        if not can_create:
            response["message"] = "Для создания тренировочных программ необходимо настроить профиль тренера"
            response["action_required"] = "Заполните информацию о ваших сертификатах и опыте работы в профиле тренера"
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error checking training creation permissions: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось проверить права на создание тренировок"
        ) 