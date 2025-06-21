# API Documentation: 

# GET /survey-data - Get survey configuration data

## 🎯 Purpose
The endpoint `GET /survey-data` returns **general settings and reference data** required for:

1. **Initialization of forms** on the frontend:
 - Lists of countries to select from
 - Valid values for fields (age, training goals, etc.)

2. **Data validation** before sending to the server:
 - Rules for validating input values
 - Required/unique fields

3. **Auto-fill** optional fields with default values


## 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/survey-data`  
**Base URL:** `https://api.example.com`  
**Full Path:** `https://api.example.com/survey-data`


## 🔐 Authentication Requirements
- **Access:** Public  
- **Authorization:** Not required  
- **Security:** No sensitive data exposed  
- **Bearer token**: Not needed for this endpoint  
*(Note: For personal data, use `/user-data` which requires authentication)*

## 🚫  What does NOT return
- User personal data (name, email, etc.)
- Session-specific data


## 📝 Parameters
None

## 📤 Example Successful Request
````http
GET /survey-data HTTP/1.1
Host: api.example.com
Accept: application/json
````


## ✅ Successful Response(200 OK)
```json
{
  "countries": [
    {
      "code": "kz",
      "name": "kazakhstan",
      "display_name": "Kazakhstan"
    }
  ],
  "validation_rules": {
    "required_fields": ["user_data.full_name"],
    "string_lengths": {
      "username": {"min": 3, "max": 50}
    }
  },
  "default_values": {
    "training_level": "beginner"
  }
}
```

## ⚠️ Possible Errors

| Code | Description | When It Occurs |
|------|-------------|----------------|
| **404** | `Survey data file not found` | The `data/survey_data.json` file is missing on the server |
| **500** | `Invalid JSON format in survey data file` | File exists but contains invalid JSON |
| **500** | `Failed to load survey data` | Any other error while reading/processing the survey file |

**Example 404 Error Response:**
```json
{
  "error": "Not Found",
  "message": "Survey data file not found",
  "status_code": 404
}
```


# GET /user-data - Get Authenticated User Data

## 🎯 Purpose
The endpoint `GET /user-data` returns **complete profile information** for authenticated users including:

1. **Personal details**:
   - Name, email, account information
   - Subscription status

2. **Training profile**:
   - Fitness goals and preferences
   - Workout history and statistics

3. **Account settings**:
   - Notification preferences
   - Privacy settings

## 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/user-data`  
**Base URL:** `https://api.example.com/api/v1`  
**Full Path:** `https://api.example.com/api/v1/user-data`


## 🔐 Authentication Requirements
- **Access:** Private (requires authentication)  
- **Authorization:** Bearer token required  
- **Security Level:** High (contains sensitive data)  

## 📝 Parameters
None required

## 📤 Example Request
```http
GET /api/v1/user-data HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
Accept-Language: en-US
````


## ✅ Successful Response(200 OK)
```json

{
  "user_profile": {
    "id": "usr_12345",
    "full_name": "Alex Johnson",
    "email": "alex.johnson@example.com",
    "username": "alexfit",
    "account_status": "active",
    "created_at": "2023-01-15T10:30:00Z",
    "last_login": "2023-11-20T14:25:00Z"
  },
  "training_profile": {
    "goals": ["strength_gain", "endurance"],
    "level": "intermediate",
    "preferences": {
      "workout_duration": "45-60_min",
      "equipment": ["dumbbells", "resistance_bands"]
    },
    "achievements": {
      "workouts_completed": 42,
      "streak_days": 7
    }
  },
  "settings": {
    "notifications": {
      "email": true,
      "push": false
    },
    "privacy": {
      "profile_visibility": "friends_only"
    }
  },
  "metadata": {
    "version": "1.2.0",
    "last_updated": "2023-11-20T08:00:00Z"
  }
}
```

## ⚠️ Error Responses

| Status Code | Error Type           | Description                      | Resolution                      |
|-------------|----------------------|----------------------------------|---------------------------------|
| `401`       | Unauthorized         | Missing or invalid token         | Provide valid Bearer token      |
| `403`       | Forbidden            | Insufficient permissions         | Check user privileges           |
| `404`       | Not Found            | User not found                   | Verify user exists              |
| `429`       | Too Many Requests    | Rate limit exceeded              | Implement backoff strategy      |
| `500`       | Server Error         | Internal server error            | Contact support                 |

