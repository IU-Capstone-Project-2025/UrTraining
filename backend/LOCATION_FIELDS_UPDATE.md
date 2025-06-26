# Location Fields Update

## Overview
Added `country` and `city` fields to the User model to capture user's geographical location.

## Changes Made

### 1. Pydantic Model Updates (`app/models/user.py`)
- Added `Country` enum with values: `"kz"`, `"ru"`, `"us"`
- Added `country` field to `PersonalData` (optional, Country enum)
- Added `city` field to `PersonalData` (optional, string 1-100 chars)

### 2. Database Model Updates (`app/models/database_models.py`)
- Added `country` column: `VARCHAR(3)` (nullable)
- Added `city` column: `VARCHAR(100)` (nullable)

### 3. Migration Script
- Created `add_location_fields_migration.py` to safely add columns to existing database
- Script checks if columns exist before adding them

### 4. Documentation Updates
- Updated `user_possible_fields_values.json` with validation rules
- Updated `user_possible_values.md` with field specifications
- Added default values (both null)

## Field Specifications

### Country Field
- **Type**: Optional string enum
- **Values**: `"kz"` (Kazakhstan), `"ru"` (Russia), `"us"` (United States)
- **Database**: `VARCHAR(3)`, nullable
- **Default**: `null`

### City Field  
- **Type**: Optional string
- **Length**: 1-100 characters
- **Database**: `VARCHAR(100)`, nullable
- **Default**: `null`

## Usage Example

```python
from app.models import User, PersonalData, Country

# Create user with location
personal_data = PersonalData(
    username="john_doe",
    full_name="John Doe",
    country=Country.KAZAKHSTAN,  # or "kz"
    city="Almaty"
)

user = User(
    personal_data=personal_data,
    # ... other required fields
)
```

## Migration Instructions

To update existing database:

```bash
# Run the migration script
python add_location_fields_migration.py
```

## API Integration

These fields will be automatically available in:
- User creation endpoints
- User profile updates  
- User responses

The fields match the form data already collected in `survey_data.json` and `coach_auth_data.json`. 