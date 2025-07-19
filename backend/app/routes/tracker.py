from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.crud import (
    save_user_schedule,
    get_user_schedule,
    get_trainings_by_date,
    delete_user_schedule,
    get_user_calendar_dates,
    debug_all_schedules,
    get_available_course_ids
)
from app.models.tracker import (
    ScheduleInstance,
    AddScheduleRequest,
    ScheduleResponse,
    TrainingByDateResponse,
    TrainingDayInfo,
    AddScheduleResponse,
    DeleteScheduleResponse
)
from app.routes.auth import get_current_user

router = APIRouter()


@router.post("/schedule", response_model=AddScheduleResponse)
async def add_schedule(
    request: AddScheduleRequest,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Добавить расписание тренировок для пользователя
    """
    try:
        print(f"📅 POST /tracker/schedule - User ID: {current_user['id']}")
        print(f"📋 Received schedule data: {request.schedule}")
        
        # Преобразуем Pydantic модели в словари для CRUD функции
        schedule_data = []
        for item in request.schedule:
            schedule_data.append({
                "course_id": item.course_id,
                "date": item.date,
                "index": item.index
            })
        
        print(f"📋 Processed schedule data: {schedule_data}")
        
        # Сохраняем расписание
        added_count = save_user_schedule(db, current_user["id"], schedule_data)
        
        return AddScheduleResponse(
            message=f"Расписание успешно добавлено",
            added_instances=added_count,
            user_id=current_user["id"]
        )
        
    except Exception as e:
        print(f"Error adding schedule: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось сохранить расписание"
        )


@router.get("/schedule", response_model=ScheduleResponse)
async def get_schedule(
    course_id: Optional[str] = Query(None, description="ID курса для фильтрации"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить расписание пользователя
    """
    try:
        print(f"📋 GET /tracker/schedule - User ID: {current_user['id']}, Course ID: {course_id}")
        
        # Получаем расписание
        schedule_db = get_user_schedule(db, current_user["id"], course_id)
        
        print(f"📊 Found {len(schedule_db)} schedule items in database")
        
        # Преобразуем в Pydantic модели
        schedule_instances = []
        for item in schedule_db:
            schedule_instances.append(ScheduleInstance(
                date=item.date,
                index=item.training_index,
                course_id=item.course_id
            ))
        
        return ScheduleResponse(
            user_id=current_user["id"],
            total_instances=len(schedule_instances),
            schedule=schedule_instances
        )
        
    except Exception as e:
        print(f"Error getting schedule: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось получить расписание"
        )


@router.get("/schedule/date/{date}", response_model=TrainingByDateResponse)
async def get_trainings_by_date_endpoint(
    date: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все тренировки на конкретную дату
    Формат даты: ДД.ММ.ГГГГ (например, 21.07.2025)
    """
    try:
        print(f"🔍 GET /tracker/schedule/date/{date} - User ID: {current_user['id']}")
        

        
        # Получаем тренировки на дату
        trainings_data = get_trainings_by_date(db, current_user["id"], date)
        
        # Преобразуем в Pydantic модели
        trainings = []
        for training in trainings_data:
            trainings.append(TrainingDayInfo(
                course_id=training["course_id"],
                course_title=training["course_title"],
                training_index=training["training_index"],
                training_day=training["training_day"]
            ))
        
        print(f"📊 Returning {len(trainings)} trainings for date '{date}'")
        
        return TrainingByDateResponse(
            date=date,
            trainings=trainings
        )
        
    except Exception as e:
        print(f"❌ Error getting trainings by date: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось получить тренировки на дату {date}"
        )


@router.delete("/schedule/{course_id}", response_model=DeleteScheduleResponse)
async def delete_schedule(
    course_id: str,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить все расписание для конкретного курса
    """
    try:
        # Удаляем расписание для курса
        deleted_count = delete_user_schedule(db, current_user["id"], course_id)
        
        return DeleteScheduleResponse(
            message=f"Расписание для курса {course_id} удалено",
            deleted_instances=deleted_count
        )
        
    except Exception as e:
        print(f"Error deleting schedule: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось удалить расписание для курса {course_id}"
        )


@router.get("/calendar", response_model=List[str])
async def get_calendar(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все даты с тренировками для отображения в календаре
    """
    try:
        # Получаем все даты с тренировками
        dates = get_user_calendar_dates(db, current_user["id"])
        
        return dates
        
    except Exception as e:
        print(f"Error getting calendar dates: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось получить календарь тренировок"
        )


@router.get("/available-courses", response_model=List[str])
async def get_available_courses(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить список всех доступных course_id для добавления в расписание
    """
    try:
        course_ids = get_available_course_ids(db)
        return course_ids
        
    except Exception as e:
        print(f"Error getting available courses: {e}")
        raise HTTPException(
            status_code=500,
            detail="Не удалось получить список доступных курсов"
        ) 