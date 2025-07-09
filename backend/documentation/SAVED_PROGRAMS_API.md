# Saved Programs API Endpoints

This document describes the new API endpoints for saving and managing training programs for trainees.

## Overview

The saved programs functionality allows trainees to save training programs they're interested in and retrieve them later. This implements a "favorites" or "bookmarks" system for training programs.

## Database Changes

A new table `saved_programs` has been added with the following structure:

```sql
CREATE TABLE saved_programs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    training_id INTEGER NOT NULL REFERENCES trainings(id),
    saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_training UNIQUE (user_id, training_id)
);
```

## Migration

To set up the database:

1. **Start the database service:**
   ```bash
   docker-compose up db -d
   ```

2. **Run the migration:**
   ```bash
   python add_saved_programs_migration.py
   ```

3. **To rollback (if needed):**
   ```bash
   python add_saved_programs_migration.py rollback
   ```

## API Endpoints

### 1. Save a Program

**Endpoint:** `POST /saved-programs/`

**Description:** Save a training program to the current user's saved list.

**Authentication:** Required (Bearer token)

**Request Body:**
```json
{
    "course_id": "string"
}
```

**Response:**
```json
{
    "message": "Программа успешно сохранена",
    "saved": true
}
```

**Error Responses:**
- `404` - Program not found
- `401` - Authentication required
- `500` - Server error

**Example Usage:**
```bash
curl -X POST "http://localhost:8000/saved-programs/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_id": "12345"}'
```

### 2. Remove a Saved Program

**Endpoint:** `DELETE /saved-programs/{course_id}`

**Description:** Remove a training program from the current user's saved list.

**Authentication:** Required (Bearer token)

**Parameters:**
- `course_id` (path) - The ID of the course to unsave

**Response:**
```json
{
    "message": "Программа удалена из сохраненных",
    "saved": false
}
```

**Example Usage:**
```bash
curl -X DELETE "http://localhost:8000/saved-programs/12345" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 3. Get Saved Programs

**Endpoint:** `GET /saved-programs/`

**Description:** Retrieve all saved training programs for the current user.

**Authentication:** Required (Bearer token)

**Query Parameters:**
- `skip` (optional) - Number of records to skip (default: 0)
- `limit` (optional) - Maximum number of records (default: 100, max: 100)

**Response:**
```json
[
    {
        "id": "string",
        "activity_type": "string",
        "course_title": "string",
        "trainer_name": "string",
        "difficulty_level": "string",
        "average_course_rating": 4.5,
        "tags": ["tag1", "tag2"],
        "program_description": "string",
        "training_plan": {...},
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
        // ... full TrainingResponse object
    }
]
```

**Example Usage:**
```bash
curl -X GET "http://localhost:8000/saved-programs/?skip=0&limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Features

- **Duplicate Prevention:** The unique constraint ensures a user can't save the same program twice
- **Authentication Required:** All endpoints require valid authentication
- **Pagination Support:** The get saved programs endpoint supports pagination
- **Full Program Details:** Saved programs return complete training information
- **Idempotent Operations:** Saving an already saved program won't cause errors

## Error Handling

All endpoints include comprehensive error handling:

- **Authentication Errors:** 401 status for missing/invalid tokens
- **Not Found Errors:** 404 status for non-existent programs
- **Server Errors:** 500 status for database or internal errors
- **Validation Errors:** 422 status for invalid request data

## Integration Notes

1. **Frontend Integration:** These endpoints can be used to implement:
   - "Save" button on training program cards
   - "Saved Programs" section in user dashboard
   - Heart/bookmark icons that toggle save status

2. **Database Performance:** Indexes are created on `user_id` and `training_id` for optimal query performance

3. **Data Consistency:** Foreign key constraints ensure data integrity between users, trainings, and saved programs

## Testing

To test the endpoints:

1. **Get an authentication token** by logging in via `/auth/login`
2. **Find a training program ID** via `/trainings/` endpoint
3. **Save the program** using the save endpoint
4. **Retrieve saved programs** to verify it was saved
5. **Unsave the program** to test removal

## Status

✅ Database model created
✅ CRUD functions implemented  
✅ API endpoints created
✅ Migration script ready
✅ **Separate router created (`/saved-programs/`) - FIXED path conflicts**
⏳ Database migration (requires running database)
⏳ Testing (requires running application)

## Changes Made

**✅ RESOLVED:** Fixed the path conflict issue by moving saved programs endpoints to a separate router:
- **Old paths:** `/trainings/save`, `/trainings/saved`, `/trainings/{id}/save`
- **New paths:** `/saved-programs/`, `/saved-programs/`, `/saved-programs/{id}`
- **FastAPI Documentation:** Now appears as separate "Saved Programs" section 