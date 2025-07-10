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

# PUT /user-data - Update User Data (Preferred Method)

###  🎯 Purpose
The endpoint `PUT /user-data` allows authenticated users to **update their complete profile information** using proper HTTP semantics for resource updates, including:

1. **Personal details**:
   - Username, full name, email
   - Country and city information

2. **Training profile**:
   - Basic information (gender, age, height, weight)
   - Training goals and experience level
   - Preferences and health information
   - Training types interest levels (1-5 scale)

3. **Partial updates**:
   - Update only the fields you need to change
   - Other fields remain unchanged

###  🌐 HTTP Method and URL
**Method:** `PUT`  
**Endpoint:** `/user-data`  

###  🔐 Authentication Requirements
- **Access:** Private (requires authentication)  
- **Authorization:** Bearer token required  
- **Security Level:** High (contains sensitive operations)  
- **Permissions:** Only owner can update their data 

###  📝 Request Body Schema
All fields are optional - include only the fields you want to update:

```json
{
  "username": "string (3-50 chars, optional)",
  "full_name": "string (2-100 chars, optional)",
  "email": "string (valid email, optional)",
  "country": "enum ['kz', 'ru', 'us'] (optional)",
  "city": "enum [valid cities for selected country] (optional)",
  "training_profile": {
    "basic_information": {
      "gender": "enum ['male', 'female'] (optional)",
      "age": "integer (13-100, optional)",
      "height_cm": "integer (100-250, optional)",
      "weight_kg": "float (30-300, optional)"
    },
    "training_goals": ["array of enums (max 2 items, optional)"],
    "training_experience": {
      "level": "enum ['beginner', 'intermediate', 'advanced'] (optional)",
      "frequency_last_3_months": "enum (optional)"
    },
    "preferences": {
      "training_location": "enum ['gym', 'home', 'outdoor', 'mixed'] (optional)",
      "location_details": "enum (optional)",
      "session_duration": "enum (optional)"
    },
    "health": {
      "joint_back_problems": "boolean (optional)",
      "chronic_conditions": "boolean (optional)",
      "health_details": "string (max 1000 chars, optional)"
    },
    "training_types": {
      "strength_training": "integer (1-5, optional)",
      "cardio": "integer (1-5, optional)",
      "hiit": "integer (1-5, optional)",
      "yoga_pilates": "integer (1-5, optional)",
      "functional_training": "integer (1-5, optional)",
      "stretching": "integer (1-5, optional)"
    }
  }
}
```

###  📤 Example Request - Update only username and age
```http
PUT /user-data HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "username": "new_username_123",
  "training_profile": {
    "basic_information": {
      "age": 28
    }
  }
}
```

###  📤 Example Request - Update training goals and preferences
```http
PUT /user-data HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "training_profile": {
    "training_goals": ["weight_loss", "improve_endurance"],
    "preferences": {
      "training_location": "gym",
      "session_duration": "45_60_min"
    },
    "training_types": {
      "cardio": 5,
      "strength_training": 3
    }
  }
}
```

###  ✅ Successful Response (200 OK)
```json
{
  "message": "User data updated successfully",
  "updated_fields": {
    "user_profile": true,
    "training_profile": true
  }
}
```

### ⚠️ Error Responses

| Status Code | Error Type           | Description                                  | Resolution                      |
|-------------|----------------------|----------------------------------------------|---------------------------------|
| `400`       | Validation Error     | Invalid field values or constraints          | Check request format            |
| `400`       | Duplicate Data       | Username/email already exists                | Choose different values         |
| `401`       | Unauthorized         | Invalid or missing authentication token      | Provide valid Bearer token      |
| `404`       | User Not Found       | User account not found                       | Check user authentication       |
| `500`       | Server Error         | Internal server error                        | Contact support                 |

### 📝 Field Validation Rules

#### Username
- 3-50 characters
- Must be unique across all users
- Alphanumeric characters and underscores allowed

#### Email  
- Valid email format required
- Must be unique across all users
- Will be converted to lowercase

#### Country & City
- City must belong to the selected country
- Supported countries: Kazakhstan (kz), Russia (ru), USA (us)

#### Training Types (1-5 Scale)
- 1 = Not interested
- 2 = Slightly interested  
- 3 = Moderately interested
- 4 = Very interested
- 5 = Extremely interested

### 💡 Usage Tips

1. **Partial Updates**: You can update just one field or multiple fields in a single request
2. **Atomic Updates**: All updates in one request are processed together - if any field fails validation, nothing is updated
3. **Idempotent**: Multiple identical PUT requests will have the same result
4. **Performance**: Only include fields you actually want to change to minimize processing

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
- `name`: User's full name (from user.full_name)
- `profile_picture`: From trainer_profile.profile_picture
- `rating`: From trainer_profile.experience.rating (default: 5.0)
- `reviews`: From trainer_profile.reviews_count (default: 0)
- `years`: From trainer_profile.experience.years (default: 0)
- `badges`: From trainer_profile.badges + any additional badges from request

#### Auto-filled in `course_info`:
- `author`: User's full name (from user.full_name)
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
    "author": "John Smith",  // Auto-filled from user.full_name
    "description": "A comprehensive workout program for beginners",
    "rating": 4.8,  // Auto-filled from trainer_profile.experience.rating
    "reviews": 25   // Auto-filled from trainer_profile.reviews_count
  },
  "training_plan": [...],
  "coach_data": {
    "name": "John Smith",  // Auto-filled from user.full_name
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

---

# GET /auth/validation/trainer-profile - Get Trainer Profile Validation Rules

### 🎯 Purpose
The endpoint `GET /auth/validation/trainer-profile` returns **comprehensive validation rules** for the trainer profile, including:

1. **Field-level validation**:
   - Data types, required fields, length constraints
   - Format requirements (URLs, patterns, enums)
   - Min/max values for numeric fields

2. **Cross-field validation**:
   - Business logic rules between related fields
   - Consistency checks (e.g., rating vs experience)

3. **Dynamic validation data**:
   - Current enum values (certification types, specializations)
   - Supported formats and protocols

### 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/auth/validation/trainer-profile`

### 🔐 Authentication Requirements
- **Access:** Public (no authentication required)  
- **Authorization:** Not required  
- **Security:** No sensitive data exposed  
- **Purpose**: For frontend form validation and UI generation

### 📝 Parameters
None

### 📤 Example Request
```http
GET /auth/validation/trainer-profile HTTP/1.1
Host: api.example.com
Accept: application/json
```

### ✅ Successful Response (200 OK)
```json
{
  "message": "Validation rules for trainer profile",
  "model": "TrainerProfile",
  "validation_rules": {
    "profile_picture": {
      "type": "string",
      "required": false,
      "nullable": true,
      "max_length": 500,
      "format": "url",
      "supported_protocols": ["http", "https"],
      "supported_formats": ["jpg", "jpeg", "png", "webp", "gif"],
      "pattern": "^https?://[^\\s/$.?#].[^\\s]*$",
      "description": "URL ссылка на фото профиля тренера",
      "example": "https://example.com/trainer-photo.jpg"
    },
    "certification": {
      "type": "object",
      "required": true,
      "properties": {
        "Type": {
          "type": "enum",
          "required": true,
          "allowed_values": ["ISSA", "ACE", "NASM", "ACSM", "NSCA", "CSCS", "PTA Global", "Other"],
          "description": "Тип сертификации тренера"
        },
        "Level": {
          "type": "enum",
          "required": true,
          "allowed_values": ["Basic", "Intermediate", "Advanced", "Master", "Expert"],
          "description": "Уровень сертификации"
        }
      },
      "description": "Информация о сертификации тренера"
    },
    "experience": {
      "type": "object",
      "required": true,
      "properties": {
        "Years": {
          "type": "integer",
          "required": true,
          "min_value": 0,
          "max_value": 50,
          "description": "Количество лет опыта в тренерской деятельности"
        },
        "Specialization": {
          "type": "string",
          "required": true,
          "min_length": 2,
          "max_length": 200,
          "max_specializations": 5,
          "allowed_values": [
            "Strength Training", "Cardio Training", "HIIT", "Yoga", "Pilates",
            "Functional Training", "CrossFit", "Bodybuilding", "Powerlifting",
            "Olympic Weightlifting", "Sports Performance", "Rehabilitation",
            "Nutrition Coaching", "Group Fitness", "Personal Training",
            "Martial Arts", "Swimming", "Running/Endurance", "Flexibility/Stretching",
            "Weight Loss", "Muscle Gain", "Senior Fitness", "Youth Fitness",
            "Pre/Postnatal Fitness", "Other"
          ],
          "format": "comma_separated",
          "pattern": "^[a-zA-Zа-яА-Я0-9\\s\\-,\\.]+$",
          "description": "Специализация тренера (можно указать до 5 через запятую)",
          "example": "Strength Training, Functional Training"
        },
        "Courses": {
          "type": "integer",
          "required": true,
          "min_value": 0,
          "max_value": 10000,
          "description": "Количество созданных/проведенных курсов"
        },
        "Rating": {
          "type": "float",
          "required": true,
          "min_value": 0.0,
          "max_value": 5.0,
          "decimal_places": 1,
          "description": "Рейтинг тренера по 5-балльной шкале",
          "cross_validation": {
            "rule": "Если Years < 1, то Rating не должен быть > 3.0",
            "message": "Новички не могут иметь рейтинг выше 3.0"
          }
        }
      },
      "description": "Информация об опыте тренера"
    },
    "badges": {
      "type": "array",
      "required": false,
      "max_items": 20,
      "items": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "required": true,
            "min_length": 1,
            "max_length": 50,
            "description": "Текст значка"
          },
          "color": {
            "type": "string",
            "required": true,
            "format": "hex_color",
            "pattern": "^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
            "description": "Цвет значка в hex формате",
            "example": "#FF5733"
          }
        }
      },
      "unique_items": true,
      "uniqueness_field": "text",
      "description": "Массив значков тренера (максимум 20, без дубликатов)"
    },
    "reviews_count": {
      "type": "integer",
      "required": false,
      "default": 0,
      "min_value": 0,
      "max_value": 100000,
      "read_only": true,
      "description": "Количество отзывов о тренере (устанавливается системой)"
    },
    "bio": {
      "type": "string",
      "required": false,
      "nullable": true,
      "min_length": 10,
      "max_length": 1000,
      "content_filter": true,
      "blocked_words": ["spam", "fake", "scam"],
      "pattern": "^[^\\x00-\\x1f\\x7f-\\x9f]*$",
      "description": "Биография тренера (краткое описание опыта и подхода)",
      "example": "Опытный тренер с 5-летним стажем, специализируюсь на силовых тренировках и функциональном тренинге."
    }
  },
  "general_rules": {
    "encoding": "UTF-8",
    "case_sensitivity": "case_insensitive_enums",
    "cross_field_validations": [
      {
        "fields": ["experience.Years", "experience.Rating"],
        "rule": "Years < 1 AND Rating > 3.0 = Invalid",
        "message": "Новички не могут иметь рейтинг выше 3.0"
      },
      {
        "fields": ["experience.Years", "experience.Courses"],
        "rule": "Courses > Years * 10 = Warning",
        "message": "Количество курсов кажется несоответствующим опыту"
      }
    ],
    "notes": [
      "Все enum значения проверяются регистронезависимо",
      "Специализации можно указывать через запятую",
      "URL изображений должны содержать поддерживаемые расширения",
      "Значки должны быть уникальными по тексту"
    ]
  }
}
```

### ⚠️ Possible Error Responses

| Status Code | Error Type    | Description                      | Resolution                |
|-------------|---------------|----------------------------------|---------------------------|
| `500`       | Server Error  | Failed to load validation rules  | Contact support          |

### 💡 Usage Notes

1. **Frontend Integration**: Use this endpoint to dynamically generate form validation and UI constraints
2. **Real-time Validation**: Validate user input against these rules before submitting
3. **Error Messages**: Use the provided descriptions and messages for user-friendly validation feedback
4. **Dynamic Data**: Enum values are fetched from the current system configuration
5. **Cross-field Rules**: Implement business logic validation using the cross_field_validations section

---

# GET /auth/validation/user-profile - Get User Profile Validation Rules

### 🎯 Purpose
The endpoint `GET /auth/validation/user-profile` returns **comprehensive validation rules** for the user (trainee) profile, including:

1. **Field-level validation**:
   - Data types, required fields, length constraints
   - Format requirements (patterns, enums, numeric ranges)
   - Min/max values for physical measurements and ratings

2. **Cross-field validation**:
   - Business logic rules between related fields
   - Consistency checks (e.g., city-country matching, BMI validation)
   - Training level vs frequency validation

3. **Dynamic validation data**:
   - Current enum values for locations, goals, training types
   - Supported countries and cities mapping

### 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/auth/validation/user-profile`

### 🔐 Authentication Requirements
- **Access:** Public (no authentication required)  
- **Authorization:** Not required  
- **Security:** No sensitive data exposed  
- **Purpose**: For frontend form validation and UI generation

### 📝 Parameters
None

### 📤 Example Request
```http
GET /auth/validation/user-profile HTTP/1.1
Host: api.example.com
Accept: application/json
```

### ✅ Successful Response (200 OK)
```json
{
  "message": "Validation rules for user profile",
  "model": "User",
  "validation_rules": {
    "personal_data": {
      "type": "object",
      "required": true,
      "properties": {
        "username": {
          "type": "string",
          "required": true,
          "min_length": 3,
          "max_length": 50,
          "pattern": "^[a-zA-Z0-9_-]+$",
          "description": "Уникальное имя пользователя",
          "example": "fitness_user123"
        },
        "full_name": {
          "type": "string",
          "required": true,
          "min_length": 2,
          "max_length": 100,
          "pattern": "^[a-zA-Zа-яА-Я\\s\\-']+$",
          "description": "Полное имя пользователя",
          "example": "Иван Петров"
        },
        "country": {
          "type": "enum",
          "required": false,
          "nullable": true,
          "allowed_values": ["kz", "ru", "us"],
          "description": "Страна проживания"
        },
        "city": {
          "type": "enum",
          "required": false,
          "nullable": true,
          "allowed_values": ["Almaty", "Nur-Sultan", "Shymkent", "Moscow", "Saint Petersburg", "New York", "Los Angeles", "..."],
          "description": "Город проживания",
          "cross_validation": {
            "rule": "Город должен соответствовать выбранной стране",
            "mapping": "CITY_COUNTRY_MAP"
          }
        }
      },
      "description": "Персональные данные пользователя"
    },
    "basic_information": {
      "type": "object",
      "required": true,
      "properties": {
        "gender": {
          "type": "enum",
          "required": true,
          "allowed_values": ["male", "female"],
          "description": "Пол пользователя"
        },
        "age": {
          "type": "integer",
          "required": true,
          "min_value": 13,
          "max_value": 100,
          "description": "Возраст в годах"
        },
        "height_cm": {
          "type": "integer",
          "required": true,
          "min_value": 100,
          "max_value": 250,
          "description": "Рост в сантиметрах"
        },
        "weight_kg": {
          "type": "float",
          "required": true,
          "min_value": 30.0,
          "max_value": 300.0,
          "decimal_places": 1,
          "description": "Вес в килограммах"
        }
      },
      "description": "Базовая физическая информация"
    },
    "training_goals": {
      "type": "array",
      "required": true,
      "min_items": 1,
      "max_items": 5,
      "items": {
        "type": "enum",
        "allowed_values": [
          "weight_loss", "muscle_gain", "maintain_fitness", 
          "improve_endurance", "improve_flexibility", 
          "competition_preparation", "strength_building", "rehabilitation"
        ],
        "description": "Цель тренировок"
      },
      "unique_items": true,
      "description": "Цели тренировок (от 1 до 5)",
      "examples": ["weight_loss", "muscle_gain", "improve_endurance"]
    },
    "training_experience": {
      "type": "object",
      "required": true,
      "properties": {
        "level": {
          "type": "enum",
          "required": true,
          "allowed_values": ["beginner", "intermediate", "advanced"],
          "description": "Уровень подготовки"
        },
        "frequency_last_3_months": {
          "type": "enum",
          "required": true,
          "allowed_values": [
            "not_trained", "1_2_times_week", "3_4_times_week", 
            "5_6_times_week", "daily"
          ],
          "description": "Частота тренировок за последние 3 месяца"
        }
      },
      "description": "Опыт и частота тренировок"
    },
    "preferences": {
      "type": "object",
      "required": true,
      "properties": {
        "training_location": {
          "type": "enum",
          "required": true,
          "allowed_values": ["gym", "home", "outdoor", "mixed"],
          "description": "Предпочитаемое место тренировок"
        },
        "location_details": {
          "type": "enum",
          "required": true,
          "allowed_values": [
            "full_fitness_center", "basic_gym", "home_equipment", 
            "no_equipment", "park_outdoor"
          ],
          "description": "Детали места тренировок"
        },
        "session_duration": {
          "type": "enum",
          "required": true,
          "allowed_values": [
            "15_30_min", "30_45_min", "45_60_min", 
            "60_90_min", "90+_min"
          ],
          "description": "Предпочитаемая продолжительность тренировки"
        }
      },
      "description": "Предпочтения по тренировкам"
    },
    "health": {
      "type": "object",
      "required": true,
      "properties": {
        "joint_back_problems": {
          "type": "boolean",
          "required": true,
          "description": "Наличие проблем с суставами или спиной"
        },
        "chronic_conditions": {
          "type": "boolean",
          "required": true,
          "description": "Наличие хронических заболеваний"
        },
        "health_details": {
          "type": "string",
          "required": false,
          "nullable": true,
          "max_length": 500,
          "description": "Дополнительная информация о здоровье",
          "example": "Проблемы с коленным суставом после травмы"
        }
      },
      "description": "Информация о здоровье и ограничениях"
    },
    "training_types": {
      "type": "object",
      "required": true,
      "properties": {
        "strength_training": {
          "type": "integer",
          "required": true,
          "min_value": 1,
          "max_value": 5,
          "description": "Интерес к силовым тренировкам (1-5)"
        },
        "cardio": {
          "type": "integer",
          "required": true,
          "min_value": 1,
          "max_value": 5,
          "description": "Интерес к кардио тренировкам (1-5)"
        },
        "hiit": {
          "type": "integer",
          "required": true,
          "min_value": 1,
          "max_value": 5,
          "description": "Интерес к HIIT тренировкам (1-5)"
        },
        "yoga_pilates": {
          "type": "integer",
          "required": true,
          "min_value": 1,
          "max_value": 5,
          "description": "Интерес к йоге/пилатесу (1-5)"
        },
        "functional_training": {
          "type": "integer",
          "required": true,
          "min_value": 1,
          "max_value": 5,
          "description": "Интерес к функциональным тренировкам (1-5)"
        },
        "stretching": {
          "type": "integer",
          "required": true,
          "min_value": 1,
          "max_value": 5,
          "description": "Интерес к растяжке (1-5)"
        }
      },
      "description": "Уровень интереса к различным типам тренировок"
    },
    "trainer_profile": {
      "type": "object",
      "required": false,
      "nullable": true,
      "description": "Профиль тренера (если пользователь является тренером)",
      "properties": {
        "message": "Для валидации профиля тренера используйте GET /auth/validation/trainer-profile"
      }
    }
  },
  "general_rules": {
    "encoding": "UTF-8",
    "case_sensitivity": "case_insensitive_enums",
    "cross_field_validations": [
      {
        "fields": ["personal_data.city", "personal_data.country"],
        "rule": "Город должен соответствовать стране",
        "message": "Выберите город из указанной страны или измените страну"
      },
      {
        "fields": ["basic_information.age", "basic_information.weight_kg", "basic_information.height_cm"],
        "rule": "BMI = weight_kg / (height_cm/100)^2 должен быть в разумных пределах",
        "message": "Проверьте корректность введенных данных о росте и весе"
      },
      {
        "fields": ["training_experience.level", "training_experience.frequency_last_3_months"],
        "rule": "Продвинутый уровень должен соответствовать регулярным тренировкам",
        "message": "Уровень подготовки должен соответствовать частоте тренировок"
      }
    ],
    "validation_order": [
      "personal_data",
      "basic_information", 
      "training_goals",
      "training_experience",
      "preferences",
      "health",
      "training_types",
      "trainer_profile"
    ],
    "required_for_recommendations": [
      "basic_information.gender",
      "basic_information.age", 
      "training_experience.level",
      "training_types"
    ],
    "notes": [
      "Все enum значения проверяются регистронезависимо",
      "Цели тренировок могут быть выбраны в количестве от 1 до 5",
      "Город автоматически валидируется на соответствие стране",
      "Типы тренировок оцениваются по шкале от 1 до 5",
      "Профиль тренера опционален и валидируется отдельно"
    ]
  }
}
```

### ⚠️ Possible Error Responses

| Status Code | Error Type    | Description                      | Resolution                |
|-------------|---------------|----------------------------------|---------------------------|
| `500`       | Server Error  | Failed to load validation rules  | Contact support          |

### 💡 Usage Notes

1. **Frontend Integration**: Use this endpoint to dynamically generate form validation and UI constraints for user registration/profile editing
2. **Real-time Validation**: Validate user input against these rules before submitting profile data
3. **Error Messages**: Use the provided descriptions and messages for user-friendly validation feedback
4. **Dynamic Data**: Enum values and city-country mappings are fetched from the current system configuration
5. **Cross-field Rules**: Implement business logic validation using the cross_field_validations section
6. **Training Recommendations**: Fields marked in `required_for_recommendations` are essential for generating personalized training programs
7. **City-Country Validation**: Automatically validate city selection against the chosen country using the provided mapping
8. **BMI Validation**: Implement reasonable BMI checks to catch potential data entry errors

---


