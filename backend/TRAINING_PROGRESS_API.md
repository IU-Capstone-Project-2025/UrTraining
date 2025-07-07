# Training Progress API Endpoints

Система прогресса по тренировкам позволяет пользователям отмечать выполненные items в training_plan и отслеживать свой прогресс.

## Концепция

- **Training Plan**: каждая тренировка содержит `training_plan` - массив объектов (items)
- **Item**: один элемент плана тренировок (например, "Week 1: Day 1 - Full Body Circuit")
- **Progress**: количество выполненных items / общее количество items * 100%
- **Item Numbering**: items нумеруются с 0 (первый item = 0, второй = 1, и т.д.)

## Database Structure

Новая таблица `training_progress`:

```sql
CREATE TABLE training_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    training_id INTEGER NOT NULL REFERENCES trainings(id),
    completed_items JSONB DEFAULT '[]'::jsonb,  -- [0, 1, 3, 5] - номера выполненных items
    total_items INTEGER DEFAULT 0,             -- общее количество items в training_plan
    progress_percentage REAL DEFAULT 0.0,      -- процент прогресса (0.0 - 100.0)
    last_completed_item INTEGER,               -- номер последнего выполненного item
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_training_progress UNIQUE (user_id, training_id)
);
```

## API Endpoints

### 1. Update Progress

**Endpoint:** `POST /progress/update`

**Description:** Отметить item как выполненный

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
    "course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5",
    "item_number": 2
}
```

**Response:**
```json
{
    "message": "Item 2 отмечен как выполненный. Прогресс: 50.0%",
    "progress": {
        "course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5",
        "total_items": 6,
        "completed_items": [0, 1, 2],
        "progress_percentage": 50.0,
        "last_completed_item": 2,
        "started_at": "2024-01-01T10:00:00",
        "last_updated": "2024-01-01T12:30:00"
    }
}
```

**Validation:**
- `item_number` должен быть >= 0
- `item_number` должен быть < общего количества items в тренировке
- Если item уже выполнен, повторное выполнение не изменит прогресс

**Example:**
```bash
curl -X POST "http://localhost:8000/progress/update" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5", "item_number": 2}'
```

### 2. Get Training Progress

**Endpoint:** `GET /progress/{course_id}`

**Description:** Получить прогресс по конкретной тренировке

**Authentication:** Required (Bearer token)

**Response:**
```json
{
    "course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5",
    "total_items": 6,
    "completed_items": [0, 1, 2],
    "progress_percentage": 50.0,
    "last_completed_item": 2,
    "started_at": "2024-01-01T10:00:00",
    "last_updated": "2024-01-01T12:30:00"
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/progress/c217bc40-7553-42f9-90cd-339013cfe3b5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Get All Progress

**Endpoint:** `GET /progress/`

**Description:** Получить прогресс по всем тренировкам пользователя

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (optional) - Number of records to skip (default: 0)
- `limit` (optional) - Maximum number of records (default: 100, max: 100)

**Response:**
```json
[
    {
        "course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5",
        "total_items": 6,
        "completed_items": [0, 1, 2],
        "progress_percentage": 50.0,
        "last_completed_item": 2,
        "started_at": "2024-01-01T10:00:00",
        "last_updated": "2024-01-01T12:30:00"
    },
    {
        "course_id": "another-course-id",
        "total_items": 10,
        "completed_items": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "progress_percentage": 100.0,
        "last_completed_item": 9,
        "started_at": "2023-12-01T09:00:00",
        "last_updated": "2024-01-01T15:00:00"
    }
]
```

**Example:**
```bash
curl -X GET "http://localhost:8000/progress/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 4. Reset Progress

**Endpoint:** `POST /progress/reset`

**Description:** Сбросить прогресс по тренировке

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
    "course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5"
}
```

**Response:**
```json
{
    "message": "Прогресс успешно сброшен"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/progress/reset" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_id": "c217bc40-7553-42f9-90cd-339013cfe3b5"}'
```

## Business Logic

### Progress Calculation

```
progress_percentage = (completed_items.length / total_items) * 100
```

### Item Validation

- Items нумеруются с 0
- Максимальный номер item = `len(training_plan) - 1`
- При попытке отметить несуществующий item возвращается ошибка 400

### Auto-Creation

- При первом обновлении прогресса автоматически создается запись в `training_progress`
- `total_items` вычисляется из `len(training.training_plan)`

## Error Handling

| Status Code | Description | Example |
|-------------|-------------|---------|
| 400 | Invalid item number | `Item number 10 is invalid. Must be between 0 and 5` |
| 404 | Training not found | `Тренировка с ID course-123 не найдена` |
| 401 | Authentication required | `Could not validate credentials` |
| 500 | Server error | `Внутренняя ошибка сервера` |

## Migration

To set up the database:

```bash
# Run the migration
python add_training_progress_migration.py

# To rollback (if needed)
python add_training_progress_migration.py rollback
```

## Frontend Integration Examples

### Progress Bar
```javascript
// Get progress and display progress bar
const progress = await fetch('/progress/course-id', {
  headers: { 'Authorization': `Bearer ${token}` }
}).then(r => r.json());

// Progress bar width
const progressWidth = `${progress.progress_percentage}%`;

// Items completed vs total
const completedText = `${progress.completed_items.length} / ${progress.total_items}`;
```

### Mark Item as Complete
```javascript
// User clicks "Mark as Complete" on item 3
const markComplete = async (courseId, itemNumber) => {
  const response = await fetch('/progress/update', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      course_id: courseId,
      item_number: itemNumber
    })
  });
  
  const result = await response.json();
  console.log(result.message); // "Item 3 отмечен как выполненный. Прогресс: 66.7%"
};
```

### Check if Item is Completed
```javascript
// Check if specific item is completed
const isItemCompleted = (progress, itemNumber) => {
  return progress.completed_items.includes(itemNumber);
};

// Usage
if (isItemCompleted(progress, 2)) {
  // Show checkmark icon
} else {
  // Show incomplete icon
}
```

## Status

✅ Database model created (`TrainingProgress`)
✅ CRUD functions implemented
✅ API endpoints created (`/progress/update`, `/progress/{course_id}`, etc.)
✅ Validation logic implemented (item number bounds checking)
✅ Auto-creation of progress records
✅ Migration script ready
✅ Separate router with dedicated endpoints
⏳ Database migration (requires running database)
⏳ Testing (requires running application) 