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
    TrainingCreate
)
from app.routes.auth import get_current_user

router = APIRouter()


# Pydantic модель для краткой информации о тренировке (для каталога)
class TrainingSummary(BaseModel):
    id: int
    activity_type: str
    course_title: str
    trainer_name: str
    difficulty_level: str
    average_course_rating: float
    tags: List[str]
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
    Возвращает только основную информацию: тип активности, название курса, имя тренера и др.
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
                activity_type=training.activity_type,
                course_title=training.course_title,
                trainer_name=training.trainer_name,
                difficulty_level=training.difficulty_level,
                average_course_rating=training.average_course_rating,
                tags=training.tags or [],
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
        training = get_training_with_trainer_info(db, training_id)
        
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Тренировочная программа с ID {training_id} не найдена"
            )
        
        # Используем model_validate для создания из SQLAlchemy объекта
        training_dict = {
            "activity_type": training.activity_type,
            "program_goal": training.program_goal,
            "training_environment": training.training_environment,
            "difficulty_level": training.difficulty_level,
            "course_duration_weeks": training.course_duration_weeks,
            "weekly_training_frequency": training.weekly_training_frequency,
            "average_workout_duration": training.average_workout_duration,
            "age_group": training.age_group,
            "gender_orientation": training.gender_orientation,
            "physical_limitations": training.physical_limitations,
            "required_equipment": training.required_equipment,
            "course_language": training.course_language,
            "visual_content": training.visual_content,
            "trainer_feedback_options": training.trainer_feedback_options,
            "tags": training.tags,
            "average_course_rating": training.average_course_rating,
            "active_participants": training.active_participants,
            "number_of_reviews": training.number_of_reviews,
            "certification": training.certification,
            "experience": training.experience,
            "trainer_name": training.trainer_name,
            "course_title": training.course_title,
            "program_description": training.program_description,
            "training_plan": training.training_plan,
            "id": training.course_id,
            "db_id": training.id,
            "user_id": training.user_id,
            "created_at": training.created_at.isoformat() if training.created_at else None,
            "updated_at": training.updated_at.isoformat() if training.updated_at else None
        }
        
        return TrainingResponse(**training_dict)
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching training details: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить детали тренировки"
        )


@router.post("/", response_model=TrainingResponse, summary="Create Training")
async def create_training_program(
    training_data: TrainingCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ## Создать тренировочную программу
    
    Создает новую тренировочную программу в новом формате JSON.
    Все поля обязательны согласно структуре курса.
    
    **Требует авторизации.**
    """
    try:
        # Преобразуем Pydantic модель в словарь
        training_dict = training_data.model_dump()
        
        # Создаем тренировку
        db_training = create_training(db, training_dict, current_user["id"])
        
        # Создаем ответ используя правильную структуру
        response_dict = {
            "activity_type": db_training.activity_type,
            "program_goal": db_training.program_goal,
            "training_environment": db_training.training_environment,
            "difficulty_level": db_training.difficulty_level,
            "course_duration_weeks": db_training.course_duration_weeks,
            "weekly_training_frequency": db_training.weekly_training_frequency,
            "average_workout_duration": db_training.average_workout_duration,
            "age_group": db_training.age_group,
            "gender_orientation": db_training.gender_orientation,
            "physical_limitations": db_training.physical_limitations,
            "required_equipment": db_training.required_equipment,
            "course_language": db_training.course_language,
            "visual_content": db_training.visual_content,
            "trainer_feedback_options": db_training.trainer_feedback_options,
            "tags": db_training.tags,
            "average_course_rating": db_training.average_course_rating,
            "active_participants": db_training.active_participants,
            "number_of_reviews": db_training.number_of_reviews,
            "certification": db_training.certification,
            "experience": db_training.experience,
            "trainer_name": db_training.trainer_name,
            "course_title": db_training.course_title,
            "program_description": db_training.program_description,
            "training_plan": db_training.training_plan,
            "id": db_training.course_id,
            "db_id": db_training.id,
            "user_id": db_training.user_id,
            "created_at": db_training.created_at.isoformat() if db_training.created_at else None,
            "updated_at": db_training.updated_at.isoformat() if db_training.updated_at else None
        }
        
        return TrainingResponse(**response_dict)
        
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
        
        # Создаем ответ используя правильную структуру
        response_dict = {
            "activity_type": updated_training.activity_type,
            "program_goal": updated_training.program_goal,
            "training_environment": updated_training.training_environment,
            "difficulty_level": updated_training.difficulty_level,
            "course_duration_weeks": updated_training.course_duration_weeks,
            "weekly_training_frequency": updated_training.weekly_training_frequency,
            "average_workout_duration": updated_training.average_workout_duration,
            "age_group": updated_training.age_group,
            "gender_orientation": updated_training.gender_orientation,
            "physical_limitations": updated_training.physical_limitations,
            "required_equipment": updated_training.required_equipment,
            "course_language": updated_training.course_language,
            "visual_content": updated_training.visual_content,
            "trainer_feedback_options": updated_training.trainer_feedback_options,
            "tags": updated_training.tags,
            "average_course_rating": updated_training.average_course_rating,
            "active_participants": updated_training.active_participants,
            "number_of_reviews": updated_training.number_of_reviews,
            "certification": updated_training.certification,
            "experience": updated_training.experience,
            "trainer_name": updated_training.trainer_name,
            "course_title": updated_training.course_title,
            "program_description": updated_training.program_description,
            "training_plan": updated_training.training_plan,
            "id": updated_training.course_id,
            "db_id": updated_training.id,
            "user_id": updated_training.user_id,
            "created_at": updated_training.created_at.isoformat() if updated_training.created_at else None,
            "updated_at": updated_training.updated_at.isoformat() if updated_training.updated_at else None
        }
        
        return TrainingResponse(**response_dict)
        
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
    
    Может удалять только создатель программы.
    Выполняется мягкое удаление (деактивация).
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
        
        # Удаляем тренировку
        success = delete_training(db, training_id)
        
        if not success:
            raise HTTPException(
                status_code=500,
                detail="Не удалось удалить тренировочную программу"
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
    
    Этот эндпоинт требует авторизации и возвращает краткую информацию о тренировках пользователя.
    """
    try:
        trainings = get_trainings_by_user(db, current_user["id"], skip, limit)
        
        # Преобразуем в формат для краткого отображения
        training_summaries = []
        for training in trainings:
            training_summaries.append(TrainingSummary(
                id=training.id,
                activity_type=training.activity_type,
                course_title=training.course_title,
                trainer_name=training.trainer_name,
                difficulty_level=training.difficulty_level,
                average_course_rating=training.average_course_rating,
                tags=training.tags or [],
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
    Проверить, может ли пользователь создавать тренировочные программы.
    
    В новом формате любой авторизованный пользователь может создавать тренировки.
    """
    try:
        return {
            "can_create": True,
            "reason": "Авторизованный пользователь может создавать тренировки"
        }
        
    except Exception as e:
        print(f"Error checking create permission: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось проверить права создания"
        ) 