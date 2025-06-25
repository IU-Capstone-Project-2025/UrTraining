# API Documentation: 

# GET /survey-data - Get survey configuration data

###  🎯 Purpose
The endpoint `GET /survey-data` returns **general settings and reference data** required for:

1. **Initialization of forms** on the frontend:
 - Lists of countries to select from
 - Valid values for fields (age, training goals, etc.)

2. **Data validation** before sending to the server:
 - Rules for validating input values
 - Required/unique fields

3. **Auto-fill** optional fields with default values


###  🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/survey-data`  



###  🔐 Authentication Requirements
- **Access:** Public  
- **Authorization:** Not required  
- **Security:** No sensitive data exposed  
- **Bearer token**: Not needed for this endpoint  
*(Note: For personal data, use `/user-data` which requires authentication)*

###  🚫  What does NOT return
- User personal data (name, email, etc.)
- Session-specific data


###  📝 Parameters
None

###  📤 Example Successful Request
````http
GET /survey-data HTTP/1.1
Host: api.example.com
Accept: application/json
````


###  ✅ Successful Response(200 OK)
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

###  ⚠️ Possible Errors

| Code | Description | When It Occurs |
|------|-------------|----------------|
| **404** | `Survey data file not found` | The `data/survey_data.json` file is missing on the server |
| **500** | `Invalid JSON format in survey data file` | File exists but contains invalid JSON |
| **500** | `Failed to load survey data` | Any other error while reading/processing the survey file |




# GET /user-data - Get Authenticated User Data

###  🎯 Purpose
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

###  🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/user-data`  



###  🔐 Authentication Requirements
- **Access:** Private (requires authentication)  
- **Authorization:** Bearer token required  
- **Security Level:** High (contains sensitive data)  

###  📝 Parameters
None required

###  📤 Example Request
```http
GET /api/v1/user-data HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
Accept-Language: en-US
````


###  ✅ Successful Response(200 OK)
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

###  ⚠️ Error Responses

| Status Code | Error Type           | Description                      | Resolution                      |
|-------------|----------------------|----------------------------------|---------------------------------|
| `500`       | Server Error         | Internal server error            | Contact support                 |

# POST /user-data - Update User Data

###  🎯 Purpose
The endpoint `POST /user-data` allows authenticated users to **update their complete profile information**, including:

1. **Personal details**:
   - Name, email
   - Account preferences

2. **Training profile**:
   - Fitness goals and preferences
   - Health information
   - Training preferences

3. **Account settings**:
   - Notification preferences
   - Privacy settings

###  🌐 HTTP Method and URL
**Method:** `POST`  
**Endpoint:** `/user-data`  


###  🔐 Authentication Requirements
- **Access:** Private (requires authentication)  
- **Authorization:** Bearer token required  
- **Security Level:** High (contains sensitive operations)  
- **Permissions:** Only owner can update their data 

###  📝 Parameters
None required

###  📤 Example Request
```POST /api/v1/user-data HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "user_profile": {
    "full_name": "Alex Johnson Updated"
  },
  "training_profile": {
    "goals": ["weight_loss", "flexibility"],
    "level": "intermediate"
  }
}
```


###  ✅ Successful Response(200 OK)
```{
  "message": "User data updated successfully",
  "updated_fields": {
    "user_profile": true,
    "training_profile": true
  },
  "user_data": {
    "id": "usr_12345",
    "full_name": "Alex Johnson Updated",
    "email": "alex.johnson@example.com"
  }
}
```

### ⚠️ Error Responses

| Status Code | Error Type           | Description                      | Resolution                      |
|-------------|----------------------|----------------------------------|---------------------------------|
| `500`       | Server Error         | Internal server error            | Contact support                 |

# Authentication 

# POST	register

###  🎯 Purpose
The endpoint `POST /register` allows new users to **create an account** in the system by providing:

1. **Basic credentials**:
   - Username and password
   - Email for account recovery

2. **Profile information**:
   - Full name for personalization
   - Future profile customization options

###  🌐 HTTP Method and URL
**Method:** `POST`  
**Endpoint:** `/register`   


###  🔐 Authentication Requirements
- **Access:** Public (no authentication required)  
- **Security Level:** Medium (handles sensitive registration data)  
- **Rate Limiting:** 5 requests/minute per IP

###  📝 Request Body Schema
```json
{
  "username": "string (3-50 chars, alphanumeric)",
  "password": "string (min 6 chars)",
  "email": "string (valid email format)",
  "full_name": "string (2-100 chars)"
}
```
###  📤 Example Request
```POST /api/v1/register HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "username": "fit_user123",
  "password": "SecurePass123!",
  "email": "user@example.com",
  "full_name": "Alex Johnson"
}
```

###  ✅ Successful Response(200 OK)
```{
  "message": "User registered successfully",
  "user_info": {
    "username": "fit_user123",
    "email": "user@example.com",
    "full_name": "Alex Johnson"
  },
  "next_steps": [
    "Verify your email (check inbox)",
    "Login at /auth/login"
  ]
}
```
###  ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `400`       | Bad Request        | Username/email already exists    | Choose different credentials     |
| `500`       | Server Error       | Registration process failed      | Contact support                  |



# POST /login - User Authentication

### 🎯 Purpose
Authenticates users and returns a JWT token for accessing protected resources.

### 🌐 HTTP Method and URL
**Method:** `POST`  
**Endpoint:** `/login`  


### 🔐 Authentication Requirements
- **Access:** Public  
- **Security Level:** High (handles credentials)  
- **Rate Limiting:** 5 attempts per minute per IP

### 📝 Request Body Schema
```json
{
  "username": "string (3-50 characters)",
  "password": "string (min 6 characters)"
}
```



###  📤 Example Request
```POST /api/v1/login HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "username": "fit_user123",
  "password": "SecurePass123!"
}
```

###  ✅ Successful Response(200 OK)
```{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user_info": {
    "username": "fit_user123",
    "email": "user@example.com",
    "full_name": "Alex Johnson",
    "is_admin": false
  }
}
```
###  ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `400`       | Bad Request        | Username/email already exists    | Choose different credentials     |
| `500`       | Server Error       | Registration process failed      | Contact support                  |



# POST	/logout

### 🎯 Purpose
Terminates the current authenticated session by invalidating the JWT access token.

### 🌐 HTTP Method and URL
**Method:** `POST`  
**Endpoint:** `/logout`    


### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Security Level:** High (session management)  

### 📝 Request Body Schema
```json
{
  "session_terminated": boolean,
  "remaining_sessions": integer
}
```
### 📊 remaining_sessions Value Mapping

| Value | Meaning                      | System Behavior                              |
|-------|------------------------------|---------------------------------------------|
| `0`   | No active sessions remaining | Automatically triggers session cleanup      |
| `1-9` | Active session count         | Enforces per-user concurrent session limit  |
| `-1`  | Unlimited sessions allowed   | Bypasses session limits (enterprise plans)  |

### 📝 Request Headers
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
###  📤 Example Request
```POST /api/v1/logout HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

###  ✅ Successful Response(200 OK)
```{
  "message": "Successfully logged out",
  "details": {
    "session_terminated": true,
    "remaining_sessions": 2
  }
}
```
###  ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `401`       | Unauthorized        | Missing/invalid token           | 	Provide valid credentials       |
| `500`       | Server Error       | Registration process failed      | Contact support                  |









# PUT /trainer-profile — Update Trainer Profile

### 🎯 Purpose  
Allows the currently authenticated user to update their trainer profile, including certificates, experience, specializations, and bio.

---

### 🌐 HTTP Method and URL  
**Method:** `PATCH`  
**Endpoint:** `/trainer-profile`  

---

### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)
- **Authorization:** Bearer token in the Authorization header

---

 

### 📝 Request Body Schema
```json
{
"trainer_profile": {
"profile_picture": "https://example.com/trainers/avatars/trainer.jpg",
"certification": {
"type": "ACE",
"level": "Advanced", 
"specialization": "Strength Training"
},
"experience": {
"years": 10,
"specialization": "Strength Training",
"courses": 15,
"rating": 4.8
},
"badges": [
{
"text": "#10 in Coaches Honor Roll",
"color": "#E7C553"
},
{
"text": "Certification approved", 
"color": "#0C1CFD"
}
],
"reviews_count": 230,
"bio": "Passionate trainer with 5 years of experience helping clients achieve their goals."
}
}

```

### ✅ Successful Response (200 OK)



```{
"message": "Trainer profile updated successfully",
"trainer_profile": {
"profile_picture": "https://example.com/trainers/avatars/trainer.jpg",
"certification": {
"type": "ACE",
"level": "Advanced", 
"specialization": "Strength Training"
},
"experience": {
"years": 10,
"specialization": "Strength Training",
"courses": 15,
"rating": 4.8
},
"badges": [
{
"text": "#10 in Coaches Honor Roll",
"color": "#E7C553"
},
{
"text": "Certification approved", 
"color": "#0C1CFD"
}
],
"reviews_count": 230,
"bio": "Passionate trainer with 5 years of experience helping clients achieve their goals."
}
}



```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|-----------------------------------|
| 404         | Not Found    | User not found                   | Check authentication and user ID  |
| 500         | Server Error | Failed to update trainer profile | Try again later or contact support|


# GET /trainer-profile — Get Current User's Trainer Profile

### 🎯 Purpose  
Retrieves the trainer profile of the currently authenticated user.  
Used to display or manage the trainer-specific information linked to the user.

---

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/trainer-profile`  


---

### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in the Authorization header  
- **Security Level:** Medium (accesses personal profile data)

---

### 📤 Example Request
```GET /api/v1/trainer-profile HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Accept: application/json
```
### ✅ Successful Response(200 OK)
```{
"message": "Trainer profile retrieved successfully",
"trainer_profile": {
"profile_picture": "https://example.com/trainers/avatars/trainer.jpg",
"certification": {
"type": "ACE",
"level": "Advanced", 
"specialization": "Strength Training"
},
"experience": {
"years": 10,
"specialization": "Strength Training",
"courses": 15,
"rating": 4.8
},
"badges": [
{
"text": "#10 in Coaches Honor Roll",
"color": "#E7C553"
},
{
"text": "Certification approved", 
"color": "#0C1CFD"
}
],
"reviews_count": 230,
"bio": "Passionate trainer with 5 years of experience helping clients achieve their goals."
}
}

```


---

### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `404`       | Not Found    | User not found                   | Verify authentication token and user existence |
| `500`       | Server Error | Failed to retrieve trainer profile | Retry later or contact support  |

---

# DELETE /trainer-profile — Delete Trainer Profile

### 🎯 Purpose  
Deletes (removes) the trainer profile of the currently authenticated user.  
After deletion, the user's trainer profile data will be set to `null`.

---

### 🌐 HTTP Method and URL  
**Method:** `DELETE`  
**Endpoint:** `/trainer-profile`  


---

### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)
- **Authorization:** Bearer token in the Authorization header

---

### 📤 Example Request
```DELETE /api/v1/trainer-profile HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Accept: application/json
```


 ### ✅ Successful Response(200 OK)
```
{
"message": "Trainer profile deleted successfully",
"trainer_profile": null
}

```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|-----------------------------------|
| 404         | Not Found    | User not found                   | Check authentication and user ID  |
| 500         | Server Error | Failed to delete trainer profile | Try again later or contact support|




# Training profile

# PUT /training-profile — Update Training Profile

### 🎯 Purpose  
Allows an authenticated user to update their detailed training profile, including physical data, goals, experience, preferences, health status, and training type interests.

### 🌐 HTTP Method and URL  
**Method:** `PUT`  
**Endpoint:** `/training-profile`  


### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in the Authorization header  
- **Security Level:** High (contains sensitive personal and health data)

### 📤 Example Request  
```PUT /api/v1/training-profile HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Content-Type: application/json
```

### ✅ Successful Response(200 OK)
```{{
"message": "Training profile updated successfully",
"training_profile": {
"basic_information": {
"gender": "female",
"age": 33,
"height_cm": 168,
"weight_kg": 62.0
},
"training_goals": [
"maintain_fitness",
"stress_reduction"
],
"training_experience": {
"level": "intermediate",
"frequency_last_3_months": "3_4_times_week"
},
"preferences": {
"training_location": "home",
"location_details": "bodyweight_only",
"session_duration": "45_60_min"
},
"health": {
"joint_back_problems": false,
"chronic_conditions": false,
"health_details": ""
},
"training_types": {
"strength_training": 4,
"cardio": 3,
"hiit": 2,
"yoga_pilates": 3,
"functional_training": 4,
"stretching": 5
}
}
}


```


### ⚠️ Possible Error Responses


| Status Code | Error Type    | Description                                | Typical Resolution                 |
|-------------|---------------|--------------------------------------------|----------------------------------- |
| `400`       | Bad Request   | Invalid or missing required fields         | Correct the request payload        |
| `500`       | Server Error  | Internal server error during update        | Retry later or contact support     |



# GET /training-profile - Get Training Profile Data

### 🎯 Purpose
Retrieves the complete training profile information for the authenticated user, including fitness goals, preferences, and health data.

### 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/training-profile`  


### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Security Level:** Medium (contains health information)  

### 📝 Request Headers
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json

```
### 📤 Example Request
```GET /api/v1/training-profile HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### ✅ Successful Response(200 OK)
```{
  "training_profile": {
    "basic_information": {
      "gender": "male",
      "age": 28,
      "height_cm": 180,
      "weight_kg": 75.5,
      "last_measured": "2023-11-20T08:15:00Z"
    },
    "goals": ["muscle_gain", "improve_flexibility"],
    "experience": {
      "level": "intermediate",
      "years_training": 2,
      "frequency": "3-4_times_week"
    },
    "preferences": {
      "training_style": "hybrid",
      "equipment": ["dumbbells", "resistance_bands"],
      "session_duration": "45-60_min"
    },
    "health_considerations": {
      "injuries": ["shoulder"],
      "limitations": "Avoid high impact exercises"
    },
    "progress_metrics": {
      "strength_level": "intermediate",
      "flexibility_score": 6.5
    }
  },
  "metadata": {
    "last_updated": "2023-11-21T09:30:15Z",
    "next_review_date": "2024-01-01"
  }
}
```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `500`       | Server Error | Data retrieval failed            | Retry later or contact support   |


# DELETE /training-programs/{training_id} - Delete Training Program

### 🎯 Purpose
Deletes (deactivates) a specific training program. Users can only delete their own programs unless they are administrators.

### 🌐 HTTP Method and URL
**Method:** `DELETE`  
**Endpoint:** `/training-programs/{training_id}`  
**Path Parameter:**  
- `training_id` (integer): ID of the training program to delete

### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Required Scopes:** `training:write`  
- **Security Level:** Medium (modifies user data)  

### 📝 Request Headers
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Accept: application/json
```
### 📤 Example Request
```DELETE /api/v1/training-programs/123 HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
### ✅ Successful Response(200 OK)
```{
  "status": "success",
  "message": "Training program successfully deleted",
  "deleted_id": 123,
  "deactivated_at": "2023-11-22T14:30:00Z"
}
```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `500`       | Server Error | Data retrieval failed            | Retry later or contact support   |
| `403`       | Forbidden    | User doesn't own the program     | Check program ownership          |
| `404`       | Not Found    | Program doesn't exist            | Verify program ID                |




# POST /training-programs - Create Training Program

### 🎯 Purpose
Creates a new training program. Requires authenticated user with a completed trainer profile.

### 🌐 HTTP Method and URL
**Method:** `POST`  
**Endpoint:** `/training-programs`  

### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Required Scopes:** `trainer:create`  
- **Prerequisite:** Completed trainer profile  

### 📝 Request Headers
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json
Accept: application/json
```

### 📤 Example Request
```POST /api/v1/training-programs HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
"title": "Summer Strength Program",
"description": "A 4-week strength-building program for intermediate athletes.",
"training_data": {
"weeks": 4,
"sessions_per_week": 3,
"focus": ["strength", "mobility"]
}
}
```


### ✅ Successful Response (201 Created)
```json
{
  "id": 123,
  "user_id": 456,
  "metadata": {
    "difficulty_level": "advanced",
    "estimated_duration": 60,
    "equipment_required": ["barbell", "bench"]
  },
  "training_data": {
    "exercises": [
      {
        "name": "Bench Press",
        "sets": 4,
        "reps": 8,
        "rest_interval": 90
      }
    ],
    "weekly_schedule": {
      "monday": ["chest", "triceps"],
      "wednesday": ["legs"]
    }
  },
  "title": "Advanced Strength Program",
  "description": "4-week strength training program",
  "created_at": "2023-11-22T14:30:00Z",
  "updated_at": "2023-11-22T14:30:00Z"
}
```
### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `500`       | Server Error | Data retrieval failed            | Retry later or contact support   |
| `403`       | Forbidden    | User doesn't own the program     | Check program ownership          |
| `404`       | Not Found    | Program doesn't exist            | Verify program ID                |



# GET /training-programs — Get Trainings Catalog

### 🎯 Purpose  
Retrieves a paginated list of all training programs with summary information.  
This endpoint is used to display a catalog of trainings, returning only key details such as title, metadata, description, and basic characteristics.

---

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/training-programs`  


---

### 🔐 Authentication  
- **Access:** Public (no authentication required)  
- Suitable for browsing available training programs.

### 📤 Example Request
```GET /api/training-programs?skip=0&limit=10&search=cardio HTTP/1.1
Host: api.example.com
Accept: application/json
```

# POST /training-programs - Create Training Program

### ✅ Successful Response (201 Created)
```json
[
{
"id": 101,
"title": "Cardio Blast",
"metadata": {
"difficulty": "beginner",
"duration_minutes": 45,
"equipment": ["treadmill", "jump rope"]
},
"description": "An intense cardio program to boost your endurance.",
"created_at": "2025-06-20T12:00:00Z"
},
{
"id": 102,
"title": "Strength Builder",
"metadata": {
"difficulty": "intermediate",
"duration_minutes": 60,
"equipment": ["dumbbells", "bench"]
},
"description": "Build muscle and strength with this comprehensive program.",
"created_at": "2025-06-18T09:30:00Z"
}
]




```
### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `500`       | Server Error | Failed to retrieve trainings catalog | Retry later or contact support   |



## GET /training-programs/user/my — Get Current User's Trainings

### 🎯 Purpose  
Retrieves a paginated list of training programs created by the currently authenticated user.  
This endpoint requires user authentication and returns summarized information about the user's own trainings.

---

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/training-programs/user/my`  


---

### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in the Authorization header  
- **Security Level:** Medium (accesses user-specific data)

---


### 📤 Example Request
```GET /api/training-programs/user/my?skip=0&limit=10 HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Accept: application/json
```

# POST /training-programs - Create Training Program

### ✅ Successful Response (201 Created)
```json
[
{
"id": 201,
"title": "Personalized Strength Plan",
"metadata": {
"difficulty": "advanced",
"duration_minutes": 60,
"equipment": ["barbell", "bench"]
},
"description": "Custom strength training program tailored for you.",
"created_at": "2025-06-15T10:00:00Z"
},
{
"id": 202,
"title": "Yoga and Flexibility",
"metadata": {
"difficulty": "beginner",
"duration_minutes": 45,
"equipment": ["mat"]
},
"description": "Relaxing yoga sessions to improve flexibility.",
"created_at": "2025-06-10T08:30:00Z"
}
]



```
### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `500`       | Server Error | Failed to retrieve user trainings | Retry later or contact support   |


## GET /training-programs/can-create — Check Training Creation Permission

### 🎯 Purpose  
Checks whether the currently authenticated user has permission to create training programs.  
This typically requires the user to have a trainer profile or administrator privileges.

---

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/training-programs/can-create`  


---

### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in the Authorization header  
- **Security Level:** Medium (checks user-specific permissions)

---

### 📤 Example Request
```GET /api/training-programs/can-create HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Accept: application/json
```

# POST /training-programs - Create Training Program

###  ✅ Successful Response (200 OK) 
```json



 
{
"can_create": true,
"has_trainer_profile": true,
"is_admin": false
}

text

Если пользователь не может создавать программы, возвращается дополнительное сообщение:

{
"can_create": false,
"has_trainer_profile": false,
"is_admin": false,
"message": "Для создания тренировочных программ необходимо настроить профиль тренера",
"action_required": "Заполните информацию о ваших сертификатах и опыте работы в профиле тренера"
}



```

---

### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `404`       | Not Found    | Пользователь не найден           | Проверьте корректность токена и пользователя |
| `500`       | Server Error | Не удалось проверить права       | Попробуйте позже или свяжитесь с поддержкой |






## Training Creation with Auto-filled Trainer Data

### POST /trainings/create

**New endpoint that automatically fills trainer data from user profile**

**Authentication Required**: Yes (Bearer token)
**Trainer Profile Required**: Yes

**Request Model**: `TrainingCreateMinimal`

This endpoint automatically fills the following fields from the authenticated user's trainer profile:

#### Auto-filled in `coach_data`:
- `name`: User's name
- `profile_picture`: From trainer_profile.profile_picture
- `rating`: From trainer_profile.experience.rating (default: 5.0)
- `reviews`: From trainer_profile.reviews_count (default: 0)
- `years`: From trainer_profile.experience.years (default: 0)
- `badges`: From trainer_profile.badges + any additional badges from request

#### Auto-filled in `course_info`:
- `author`: User's name
- `rating`: From trainer_profile.experience.rating (if not provided in request)
- `reviews`: From trainer_profile.reviews_count (if not provided in request)

**Example Request**:
```json
{
  "header_badges": {
    "training_type": [{"text": "Strength", "color": "#FF6B6B"}],
    "training_info": [{"text": "Beginner", "color": "#4ECDC4"}],
    "training_equipment": [{"text": "No Equipment", "color": "#45B7D1"}]
  },
  "course_info": {
    "id": "course_001",
    "title": "Complete Beginner Workout",
    "description": "A comprehensive workout program for beginners"
    // author, rating, reviews will be auto-filled from trainer profile
  },
  "training_plan": [
    {
      "title": "Day 1: Upper Body",
      "exercises": [
        {
          "exercise": "Push-ups",
          "repeats": "10-15",
          "sets": "3",
          "duration": "30 seconds",
          "rest": "60 seconds",
          "description": "Standard push-ups focusing on chest and arms"
        }
      ]
    }
  ],
  "coach_data": {
    // Only additional badges need to be specified
    "badges": [{"text": "Custom Badge", "color": "#FF9F43"}]
    // name, profile_picture, rating, reviews, years will be auto-filled
  }
}
```

**Example Response**:
```json
{
  "id": 1,
  "user_id": 123,
  "header_badges": {
    "training_type": [{"text": "Strength", "color": "#FF6B6B"}],
    "training_info": [{"text": "Beginner", "color": "#4ECDC4"}],
    "training_equipment": [{"text": "No Equipment", "color": "#45B7D1"}]
  },
  "course_info": {
    "id": "course_001",
    "title": "Complete Beginner Workout",
    "author": "John Smith",  // Auto-filled from user.name
    "description": "A comprehensive workout program for beginners",
    "rating": 4.8,  // Auto-filled from trainer_profile.experience.rating
    "reviews": 25   // Auto-filled from trainer_profile.reviews_count
  },
  "training_plan": [...],
  "coach_data": {
    "name": "John Smith",  // Auto-filled from user.name
    "profile_picture": "https://example.com/profile.jpg",  // Auto-filled
    "rating": 4.8,  // Auto-filled from trainer_profile.experience.rating
    "reviews": 25,  // Auto-filled from trainer_profile.reviews_count
    "years": 5,     // Auto-filled from trainer_profile.experience.years
    "badges": [
      {"text": "Certified Trainer", "color": "#27AE60"},  // From trainer_profile
      {"text": "Custom Badge", "color": "#FF9F43"}       // From request
    ]
  },
  "metadata": {},
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```


