# API Update for Location Fields

## Overview
This update adds `country` and `city` fields support to all API endpoints.

## Changes Made

### 1. API Models (`main.py`)
- Added `CountryEnum` with values: `"kz"`, `"ru"`, `"us"`
- Updated `UserDataUpdate` model to include:
  - `country: Optional[CountryEnum] = None`
  - `city: Optional[str] = Field(None, min_length=1, max_length=100)`

### 2. GET /user-data Endpoint
Now returns location fields in response:
```json
{
    "id": 1,
    "username": "john_doe",
    "full_name": "John Doe",
    "email": "john@example.com",
    "country": "kz",        // NEW FIELD
    "city": "Almaty",       // NEW FIELD
    "is_admin": false,
    // ... other fields
}
```

### 3. POST /user-data Endpoint
Now accepts location fields in request body:
```json
{
    "username": "john_doe",
    "full_name": "John Doe",
    "email": "john@example.com",
    "country": "kz",        // NEW FIELD - optional
    "city": "Almaty",       // NEW FIELD - optional
    "training_profile": {
        // ... training profile data
    }
}
```

### 4. CRUD Functions (`app/crud.py`)
- Updated `update_user_profile()` to accept `country` and `city` parameters
- Updated `create_user()` to accept `country` and `city` parameters

### 5. Auth Endpoints (`app/routes/auth.py`)
- Updated `get_current_user()` to return location fields
- Updated login response to include location fields
- Updated registration response to include location fields

## Field Validation

### Country Field
- **Type**: Optional string enum
- **Allowed Values**: `"kz"`, `"ru"`, `"us"`
- **API Request**: Send as string value
- **Response**: Returns as string value

### City Field
- **Type**: Optional string
- **Length**: 1-100 characters
- **API Request**: Send as string
- **Response**: Returns as string or `null`

## Usage Examples

### Update user location via POST /user-data:
```bash
curl -X POST "http://localhost:8000/user-data" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "country": "kz",
    "city": "Almaty"
  }'
```

### Full user update with location:
```bash
curl -X POST "http://localhost:8000/user-data" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "John Doe Updated",
    "country": "ru",
    "city": "Moscow",
    "training_profile": {
      "basic_information": {
        "age": 30
      }
    }
  }'
```

## Migration Required

Before using these fields, run the database migration:
```bash
python add_location_fields_migration.py
```

## API Documentation

The Swagger documentation (available at `/docs`) will automatically show the new fields in:
- `UserDataUpdate` schema for POST requests
- Response schemas for GET requests

## Backward Compatibility

- All existing API calls continue to work
- New fields are optional and default to `null`
- No breaking changes to existing functionality 