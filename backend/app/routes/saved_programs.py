from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel, Field

from app.database import get_db
from app.crud import (
    save_program_for_user,
    unsave_program_for_user,
    get_saved_programs_for_user,
    get_training_by_course_id,
    is_program_saved_by_user
)
from app.models.training import TrainingResponse
from app.routes.auth import get_current_user

router = APIRouter()

# Pydantic models
class SaveProgramRequest(BaseModel):
    course_id: str = Field(..., description="ID курса для сохранения")

class SaveProgramResponse(BaseModel):
    message: str
    saved: bool

class ProgramSavedStatusResponse(BaseModel):
    saved: bool    

@router.post("/{course_id}", response_model=SaveProgramResponse)
async def save_program(
    course_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Сохранить программу тренировок для текущего пользователя
    """
    try:
        # Найти тренировку по course_id
        training = get_training_by_course_id(db, course_id)
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Программа тренировок с ID {course_id} не найдена"
            )
        
        # Сохранить программу для пользователя
        saved_program = save_program_for_user(db, current_user["id"], training.id)
        
        if saved_program:
            return SaveProgramResponse(
                message="Программа успешно сохранена",
                saved=True
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Не удалось сохранить программу"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error saving program: {e}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )


@router.delete("/{course_id}", response_model=SaveProgramResponse)
async def unsave_program(
    course_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить программу тренировок из сохраненных для текущего пользователя
    """
    try:
        # Найти тренировку по course_id
        training = get_training_by_course_id(db, course_id)
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Программа тренировок с ID {course_id} не найдена"
            )
        
        # Удалить программу из сохраненных
        unsaved = unsave_program_for_user(db, current_user["id"], training.id)
        
        if unsaved:
            return SaveProgramResponse(
                message="Программа удалена из сохраненных",
                saved=False
            )
        else:
            return SaveProgramResponse(
                message="Программа не была сохранена",
                saved=False
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error unsaving program: {e}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )


@router.get("/", response_model=List[TrainingResponse])
async def get_saved_programs(
    skip: int = Query(0, ge=0, description="Количество записей для пропуска"),
    limit: int = Query(100, ge=1, le=100, description="Максимальное количество записей"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все сохраненные программы тренировок для текущего пользователя
    """
    try:
        saved_trainings = get_saved_programs_for_user(db, current_user["id"], skip, limit)
        
        # Helper function to create response dict from db training
        def create_response_dict(db_training):
            # Handle None values for certification and experience
            certification = db_training.certification
            if certification is None:
                certification = {
                    "Type": "",
                    "Level": "",
                    "Specialization": ""
                }
            
            experience = db_training.experience
            if experience is None:
                experience = {
                    "Years": 0,
                    "Specialization": "",
                    "Courses": 0,
                    "Rating": 0.0
                }
            
            return {
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
                "certification": certification,
                "experience": experience,
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

        # Преобразуем в полный формат TrainingResponse
        training_responses = []
        for training in saved_trainings:
            training_dict = create_response_dict(training)
            training_responses.append(TrainingResponse(**training_dict))
        
        return training_responses
        
    except Exception as e:
        print(f"Error fetching saved programs: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось загрузить сохраненные программы"
        ) 
    
@router.get("/{course_id}/status", response_model=ProgramSavedStatusResponse)
async def check_program_saved_status(
    course_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Проверка, сохранена ли программа тренировок пользователем
    """
    try:
        training = get_training_by_course_id(db, course_id)
        if not training:
            raise HTTPException(
                status_code=404,
                detail=f"Программа с ID {course_id} не найдена"
            )
        
        is_saved = is_program_saved_by_user(db, current_user["id"], training.id)
        return ProgramSavedStatusResponse(saved=is_saved)

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error when checking the saved status: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")