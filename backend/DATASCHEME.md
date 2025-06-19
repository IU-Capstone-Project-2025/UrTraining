# Схема базы данных UrTraining

## Подключение к базе данных

### Конфигурация

Проект использует PostgreSQL в качестве основной базы данных с возможностью fallback на SQLite для локальной разработки.

**Основные параметры подключения:**
- **База данных:** PostgreSQL 15
- **Хост:** db (в Docker контейнере) / localhost
- **Порт:** 5432
- **Пользователь:** uruser
- **Пароль:** urpassword  
- **Название БД:** urtraining

**URL подключения:**
```
postgresql://uruser:urpassword@db:5432/urtraining
```

**Fallback для локальной разработки:**
```
sqlite:///./urtraining.db
```

### Инициализация базы данных

1. **Создание таблиц:** `python init_db.py`
2. **Автоматическая инициализация:** выполняется при запуске приложения через SQLAlchemy
3. **Добавление тестовых данных:** автоматически при первом запуске

### Технологии

- **ORM:** SQLAlchemy
- **Миграции:** SQLAlchemy MetaData
- **Валидация:** Pydantic
- **Сессии:** SQLAlchemy SessionLocal

---

## Описание таблиц

### 1. Таблица `users` (Пользователи)

**Назначение:** Хранение основной информации о пользователях системы.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Уникальный идентификатор пользователя |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL, INDEX | Имя пользователя для входа |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Электронная почта |
| `hashed_password` | VARCHAR(255) | NOT NULL | Хэш пароля |
| `full_name` | VARCHAR(100) | NOT NULL | Полное имя пользователя |
| `is_active` | BOOLEAN | DEFAULT TRUE | Активен ли аккаунт |
| `is_admin` | BOOLEAN | DEFAULT FALSE | Является ли администратором |
| `created_at` | DATETIME | DEFAULT NOW() | Дата создания |
| `updated_at` | DATETIME | ON UPDATE NOW() | Дата последнего обновления |

**Связи:**
- `training_profile` (1:1) → `training_profiles.user_id`
- `active_sessions` (1:N) → `active_sessions.user_id`
- `user_course_progress` (1:N) → `user_course_progress.user_id`

---

### 2. Таблица `training_profiles` (Тренировочные профили)

**Назначение:** Детальная информация о тренировочных предпочтениях и характеристиках пользователя.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Уникальный идентификатор профиля |
| `user_id` | INTEGER | FOREIGN KEY, UNIQUE, NOT NULL | Связь с пользователем |
| `gender` | VARCHAR(10) | | Пол (male/female) |
| `age` | INTEGER | | Возраст |
| `height_cm` | INTEGER | | Рост в сантиметрах |
| `weight_kg` | FLOAT | | Вес в килограммах |
| `training_goals` | JSON | | Цели тренировок (массив строк) |
| `training_level` | VARCHAR(20) | | Уровень подготовки (beginner/intermediate/advanced) |
| `frequency_last_3_months` | VARCHAR(30) | | Частота тренировок за последние 3 месяца |
| `training_location` | VARCHAR(20) | | Место тренировок (gym/home/outdoor/mixed) |
| `location_details` | VARCHAR(30) | | Детали места тренировок |
| `session_duration` | VARCHAR(20) | | Предпочитаемая длительность сессии |
| `joint_back_problems` | BOOLEAN | | Проблемы с суставами/спиной |
| `chronic_conditions` | BOOLEAN | | Хронические заболевания |
| `health_details` | TEXT | | Дополнительная информация о здоровье |
| `strength_training` | INTEGER | | Интерес к силовым тренировкам (1-5) |
| `cardio` | INTEGER | | Интерес к кардио (1-5) |
| `hiit` | INTEGER | | Интерес к HIIT (1-5) |
| `yoga_pilates` | INTEGER | | Интерес к йоге/пилатесу (1-5) |
| `functional_training` | INTEGER | | Интерес к функциональным тренировкам (1-5) |
| `stretching` | INTEGER | | Интерес к растяжке (1-5) |
| `created_at` | DATETIME | DEFAULT NOW() | Дата создания |
| `updated_at` | DATETIME | ON UPDATE NOW() | Дата последнего обновления |

**Связи:**
- `user` (N:1) → `users.id`

**Возможные значения для enum полей:**

- **training_level:** `beginner`, `intermediate`, `advanced`
- **frequency_last_3_months:** `not_trained`, `1_2_times_week`, `3_4_times_week`, `5_6_times_week`, `daily`
- **training_location:** `gym`, `home`, `outdoor`, `mixed`
- **location_details:** `full_fitness_center`, `basic_gym`, `home_equipment`, `no_equipment`, `park_outdoor`
- **session_duration:** `15_30_min`, `30_45_min`, `45_60_min`, `60_90_min`, `90+_min`
- **training_goals:** `weight_loss`, `muscle_gain`, `maintain_fitness`, `improve_endurance`, `improve_flexibility`, `competition_preparation`, `strength_building`, `rehabilitation`

---

### 3. Таблица `active_sessions` (Активные сессии)

**Назначение:** Управление активными пользовательскими сессиями для безопасности.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Уникальный идентификатор сессии |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | Связь с пользователем |
| `token` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Токен сессии |
| `expires_at` | DATETIME | NOT NULL | Время истечения сессии |
| `created_at` | DATETIME | DEFAULT NOW() | Время создания сессии |
| `user_agent` | VARCHAR(255) | | User Agent браузера |
| `ip_address` | VARCHAR(45) | | IP адрес пользователя |

**Связи:**
- `user` (N:1) → `users.id`

---

### 4. Таблица `courses` (Курсы/Тренировки)

**Назначение:** Каталог доступных тренировочных курсов и программ.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Уникальный идентификатор курса |
| `title` | VARCHAR(255) | NOT NULL | Название курса |
| `description` | TEXT | | Описание курса |
| `duration_minutes` | INTEGER | | Длительность в минутах |
| `difficulty_level` | VARCHAR(20) | | Уровень сложности |
| `category` | VARCHAR(50) | | Категория курса |
| `video_url` | VARCHAR(255) | | Ссылка на видео |
| `thumbnail_url` | VARCHAR(255) | | Ссылка на превью изображение |
| `is_active` | BOOLEAN | DEFAULT TRUE | Активен ли курс |
| `created_at` | DATETIME | DEFAULT NOW() | Дата создания |
| `updated_at` | DATETIME | ON UPDATE NOW() | Дата последнего обновления |

**Связи:**
- `user_course_progress` (1:N) → `user_course_progress.course_id`

---

### 5. Таблица `user_course_progress` (Прогресс пользователей по курсам)

**Назначение:** Отслеживание прогресса пользователей по тренировочным курсам.

| Поле | Тип | Ограничения | Описание |
|------|-----|-------------|----------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Уникальный идентификатор записи |
| `user_id` | INTEGER | FOREIGN KEY, NOT NULL | Связь с пользователем |
| `course_id` | INTEGER | FOREIGN KEY, NOT NULL | Связь с курсом |
| `progress_percentage` | FLOAT | DEFAULT 0.0 | Процент выполнения (0.0-100.0) |
| `completed_at` | DATETIME | NULLABLE | Время завершения курса |
| `started_at` | DATETIME | DEFAULT NOW() | Время начала курса |

**Связи:**
- `user` (N:1) → `users.id`
- `course` (N:1) → `courses.id`

---

## Диаграмма связей

```
users (1) ←→ (1) training_profiles
users (1) ←→ (N) active_sessions
users (1) ←→ (N) user_course_progress
courses (1) ←→ (N) user_course_progress
```

---

## Примеры использования

### Создание пользователя с профилем
```python
# Создание пользователя
user = create_user(
    db=db,
    username="john_doe",
    email="john@example.com", 
    password="secure_password",
    full_name="John Doe"
)

# Обновление тренировочного профиля
profile_data = {
    "gender": "male",
    "age": 28,
    "height_cm": 175,
    "weight_kg": 70.0,
    "training_goals": ["muscle_gain", "strength_building"],
    "training_level": "intermediate",
    "frequency_last_3_months": "3_4_times_week",
    "training_location": "gym",
    "location_details": "full_fitness_center",
    "session_duration": "45_60_min",
    "joint_back_problems": False,
    "chronic_conditions": False,
    "strength_training": 5,
    "cardio": 3,
    "hiit": 4,
    "yoga_pilates": 2,
    "functional_training": 4,
    "stretching": 3
}
update_training_profile(db, user.id, profile_data)
```

### Инициализация базы данных
```bash
# Создание всех таблиц и добавление тестовых данных
python init_db.py

# Только создание таблиц
python -c "from app.database import engine; from app.models.database_models import Base; Base.metadata.create_all(bind=engine)"
```

---

## Заметки по безопасности

1. **Пароли:** Хранятся только в хэшированном виде
2. **Сессии:** Автоматически истекают, отслеживаются по IP и User Agent
3. **Доступ:** Разделение прав через поле `is_admin`
4. **Активность:** Контроль через поле `is_active`

---

## Настройки окружения

Создайте файл `.env` с настройками:

```env
DATABASE_URL=postgresql://uruser:urpassword@localhost:5432/urtraining
SECRET_KEY=your-secret-key-here
```

Для Docker используются настройки из `docker-compose.yml`. 