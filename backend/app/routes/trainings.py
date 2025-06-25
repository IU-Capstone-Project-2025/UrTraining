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
    TrainingUpdate,
    TrainingCreateMinimal,
    CourseInfo,
    HeaderBadges
)
from app.routes.auth import get_current_user

router = APIRouter()


# Pydantic модель для краткой информации о тренировке (для каталога)
class TrainingSummary(BaseModel):
    id: int
    header_badges: Optional[HeaderBadges] = None
    course_info: Optional[CourseInfo] = None
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True


@router.get("/", response_model=List[TrainingSummary])
async def get_trainings_catalog(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(10, ge=1, le=100, description="Максимальное количество записей"),
    search: Optional[str] = Query(None, description="Поиск по названию"),
    db: Session = Depends(get_db)
):
    """
    Получить список всех тренировочных программ с краткой информацией.
    
    Этот эндпоинт используется для отображения каталога тренировок.
    Возвращает только основную информацию: значки заголовка, информацию о курсе.
    """
    try:
        if search:
            trainings = search_trainings(db, search, skip, limit)
        else:
            trainings = get_trainings_summary(db, skip, limit)
        
        # Преобразуем в формат для краткого отображения
        training_summaries = []
        for training in trainings:
            # Обрабатываем header_badges
            header_badges = training.header_badges or {}
            try:
                training_header_badges = HeaderBadges(**header_badges)
            except Exception as e:
                print(f"Error parsing header_badges for training {training.id}: {e}")
                training_header_badges = None
            
            # Обрабатываем course_info
            course_info = training.course_info or {}
            try:
                training_course_info = CourseInfo(**course_info)
            except Exception as e:
                print(f"Error parsing course_info for training {training.id}: {e}")
                training_course_info = None
            
            training_summaries.append(TrainingSummary(
                id=training.id,
                header_badges=training_header_badges,
                course_info=training_course_info,
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
    Возвращает всю информацию включая план тренировок и данные тренера.
    """
    try:
        # Используем новую функцию для получения тренировки с информацией о тренере
        training = get_training_with_trainer_info(db, training_id)
        
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Преобразуем SQLAlchemy объект в Pydantic модель
        training_response = TrainingResponse(
            id=training.id,
            user_id=training.user_id,
            header_badges=training.header_badges or {},
            course_info=training.course_info or {},
            training_plan=training.training_plan or [],
            coach_data=training.coach_data or {},
            metadata=training.training_metadata or {},
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


@router.post("/", response_model=TrainingResponse, summary="Create Training (Auto-filled)")
async def create_training_program_minimal(
    training_data: TrainingCreateMinimal,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ## Создать тренировочную программу с автоматическим заполнением данных тренера
    
    ### Автоматически заполняется на сервере:
    
    **В coach_data (все поля):**
    - name - из имени пользователя
    - profile_picture - из trainer_profile.profile_picture  
    - rating - из trainer_profile.experience.rating
    - reviews - из trainer_profile.reviews_count
    - years - из trainer_profile.experience.years
    - badges - из trainer_profile.badges
    
    **В course_info:**
    - author - из имени пользователя
    - rating - из trainer_profile (если не указан)
    - reviews - из trainer_profile (если не указаны)
    
    ### Что нужно указать:
    - header_badges - значки заголовка
    - course_info.id, title, description - основная информация о курсе
    - training_plan - план тренировок
    - coach_data - можно оставить пустым или не указывать
    
    **Требует авторизации и настроенного профиля тренера.**
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
        
        # Создаем тренировку с автоматическим заполнением данных тренера
        db_training = create_training(db, training_dict, current_user["id"])
        
        # Возвращаем созданную тренировку
        return TrainingResponse(
            id=db_training.id,
            user_id=db_training.user_id,
            header_badges=db_training.header_badges or {},
            course_info=db_training.course_info or {},
            training_plan=db_training.training_plan or [],
            coach_data=db_training.coach_data or {},
            metadata=db_training.training_metadata or {},
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
    Обновить тренировочную программу.
    
    Может обновлять только создатель программы.
    Все поля опциональны - обновляются только переданные поля.
    """
    try:
        # Получаем существующую тренировку
        existing_training = get_training_by_id(db, training_id)
        
        if not existing_training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Проверяем права доступа - только создатель может обновлять
        if existing_training.user_id != current_user["id"]:
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав для редактирования этой тренировочной программы"
            )
        
        # Преобразуем Pydantic модель в словарь (исключая None значения)
        training_dict = training_data.model_dump(exclude_unset=True)
        
        # Обновляем тренировку
        updated_training = update_training(db, training_id, training_dict)
        
        if not updated_training:
            raise HTTPException(
                status_code=500,
                detail="Не удалось обновить тренировочную программу"
            )
        
        # Возвращаем обновленную тренировку
        return TrainingResponse(
            id=updated_training.id,
            user_id=updated_training.user_id,
            header_badges=updated_training.header_badges or {},
            course_info=updated_training.course_info or {},
            training_plan=updated_training.training_plan or [],
            coach_data=updated_training.coach_data or {},
            metadata=updated_training.training_metadata or {},
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
    Удалить (деактивировать) тренировочную программу.
    
    Может удалять только создатель программы.
    Выполняется мягкое удаление - программа остается в базе, но помечается как неактивная.
    """
    try:
        # Получаем существующую тренировку
        existing_training = get_training_by_id(db, training_id)
        
        if not existing_training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Проверяем права доступа - только создатель может удалять
        if existing_training.user_id != current_user["id"]:
            raise HTTPException(
                status_code=403,
                detail="У вас нет прав для удаления этой тренировочной программы"
            )
        
        # Выполняем мягкое удаление
        success = delete_training(db, training_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Не удалось удалить тренировочную программу"
            )
        
        return {"message": f"Тренировочная программа с ID {training_id} успешно удалена"}
        
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
    Получить мои тренировочные программы.
    
    Возвращает только тренировки, созданные текущим пользователем.
    """
    try:
        trainings = get_trainings_by_user(db, current_user["id"], skip, limit)
        
        # Преобразуем в формат для краткого отображения
        training_summaries = []
        for training in trainings:
            # Обрабатываем header_badges
            header_badges = training.header_badges or {}
            try:
                training_header_badges = HeaderBadges(**header_badges)
            except Exception as e:
                print(f"Error parsing header_badges for training {training.id}: {e}")
                training_header_badges = None
            
            # Обрабатываем course_info
            course_info = training.course_info or {}
            try:
                training_course_info = CourseInfo(**course_info)
            except Exception as e:
                print(f"Error parsing course_info for training {training.id}: {e}")
                training_course_info = None
            
            training_summaries.append(TrainingSummary(
                id=training.id,
                header_badges=training_header_badges,
                course_info=training_course_info,
                created_at=training.created_at.isoformat() if training.created_at else None
            ))
        
        return training_summaries
        
    except Exception as e:
        print(f"Error fetching user trainings: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить ваши тренировочные программы"
        )


@router.get("/can-create", response_model=dict)
async def can_create_training(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Проверить, может ли пользователь создавать тренировочные программы.
    
    Требует наличия заполненного профиля тренера.
    """
    try:
        user = get_user_by_id(db, current_user["id"])
        
        if not user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден"
            )
        
        can_create = bool(user.trainer_profile)
        
        return {
            "can_create": can_create,
            "reason": "Профиль тренера заполнен" if can_create else "Необходимо заполнить профиль тренера"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error checking create permission: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось проверить права создания"
        ) 