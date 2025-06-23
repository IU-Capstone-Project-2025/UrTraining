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

# Authentication and endpoint sessions

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




# GET /verify-token - Token Validation Endpoint

### 🎯 Purpose
Verifies the validity and authentication status of the current JWT access token.

### 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/verify-token`   


### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Security Level:** Medium (token verification)  

### 📝 Request Headers
```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
### 📤 Example Request
```GET /api/v1/verify-token HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### ✅ Successful Response(200 OK)
```{
  "token_status": "valid",
  "expires_in": 897,
  "user_info": {
    "username": "fit_user123",
    "user_id": "usr_12345",
    "is_admin": false
  },
  "token_metadata": {
    "issued_at": "2023-11-21T10:15:30Z",
    "expires_at": "2023-11-21T10:30:30Z"
  }
}
```
## ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `401`       | Unauthorized       | Invalid/expired token            | 	Re-authenticate via /login      |
| `500`       | Server Error       | Verification failed              | Contact support                  |



# Profile Management

# GET /me - Current User Profile Endpoint

### 🎯 Purpose
Retrieves the complete profile information of the currently authenticated user.

### 🌐 HTTP Method and URL
**Method:** `GET`  
**Endpoint:** `/me`  


### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Security Level:** High (returns sensitive data)  


### 📝 Request Body Schema
```json
{
  "username": "string (3-50 characters)",
  "password": "string (min 6 characters)"
}
```


### 📤 Example Request
```GET /api/v1/me HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
## ✅ Successful Response(200 OK)
```{
  "user_profile": {
    "id": "usr_12345",
    "username": "fit_user123",
    "email": "user@example.com",
    "full_name": "Alex Johnson",
    "account_status": "active",
    "created_at": "2023-01-15T10:30:00Z",
    "last_login": "2023-11-21T14:25:00Z"
  },
  "training_profile": {
    "goals": ["strength_training", "flexibility"],
    "level": "intermediate",
    "preferences": {
      "workout_duration": "45-60_min",
      "equipment": ["dumbbells", "yoga_mat"]
    }
  },
  "account_settings": {
    "notifications": {
      "email": true,
      "push": false
    },
    "privacy": {
      "profile_visibility": "friends_only"
    }
  },
  "metadata": {
    "cache_expiry": 300,
    "data_version": "1.2.0"
  }
}
```


### ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `401`       | Unauthorized       | Invalid/expired token            | 	Re-authenticate via /login      |
| `404`       | Not Found          | User profile missing             | 	Contact support                 |
| `500`       | Server Error       | Verification failed              | Contact support                  |



# PUT /profile - Update User Profile

### 🎯 Purpose
Updates the authenticated user's profile information including personal details and preferences.

### 🌐 HTTP Method and URL
**Method:** `PUT`  
**Endpoint:** `/profile`  


### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in header  
- **Permissions:** Owner only  

### 📝 Request Body Schema
```json
{
  "message": "Profile updated successfully",
  "user_info": {
    "username": "updated_username",
    "email": "updated_email@example.com",
    "full_name": "Updated Full Name"
  }
}

```

### 📤 Example Request
```GET /api/v1/me HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```
### ✅ Successful Response(200 OK)
```{
  "message": "Profile updated successfully",
  "user_info": {
    "username": "fit_user123",
    "email": "user@example.com",
    "full_name": "Alex Johnson"
  }
}

```


### ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `400`       | Bad Request        | Email already registered         | 	Use a different email address   |
| `404`       | Not Found          | User not found                   | 	Contact support                 |
| `500`       | Server Error       | Update failed                    | Retry or contact support         |


# PUT	/change-password

### 🎯 Purpose
Allows an authenticated user to change their current password to a new one.

### 🌐 HTTP Method and URL
**Method:** `PUT`  
**Endpoint:** `/change-password`  


### 🔐 Authentication Requirements
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in the Authorization header
- **Security Level** High (handles sensitive data)

### 📝 Request Body Schema
```json
{
  "current_password": "old_password",
  "new_password": "new_password"
}


```

### 📤 Example Request
```PUT /api/v1/change-password HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Content-Type: application/json
```
### ✅ Successful Response(200 OK)
```{
  "message": "Password changed successfully"
}

```


### ⚠️ Error Responses

| Status Code | Error Type         | Description                      | Typical Resolution               |
|-------------|--------------------|----------------------------------|----------------------------------|
| `400`       | Bad Request        | New password does not meet security criteria | Use a password that meets complexity requirements  |
| `500`       | Server Error       | Server error during password change          | Retry or contact support         |

# GET	/check-email-availability

### 🎯 Purpose  
Checks whether a given email address is available for registration or already taken by another user.

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/check-email-availability`  


### 📝 Request Parameters  
| Parameter | Type   | Required | Description                      |
|-----------|--------|----------|--------------------------------|
| `email`   | string | Yes      | The email address to check availability for |

### 🔐 Authentication  
- **Access:** Public (no authentication required)  
- This endpoint is usually open to allow users to check email availability before registration.

### 📤 Example Request
```GET /api/v1/check-email-availability?email=user@example.com HTTP/1.1
Host: api.example.com
Accept: application/json
```
### ✅ Successful Response(200 OK)
```{
"email": "user@example.com",
"available": true
}
```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `400`       | Bad Request  | Invalid or missing email parameter | Provide a valid email address    |
| `500`       | Server Error | Internal server error             | Retry later or contact support   |


# Training profile

## PUT /training-profile — Update Training Profile

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

# GET	/training-profile

## GET /training-profile - Get Training Profile Data

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




# Session Management

# GET /active-sessions — Retrieve Active User Sessions

### 🎯 Purpose  
Fetches a list of all active sessions for the currently authenticated user. This allows users to monitor their logged-in devices and manage session security.

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/active-sessions`  


### 🔐 Authentication Requirements  
- **Access:** Private (requires valid JWT)  
- **Authorization:** Bearer token in the Authorization header  
- **Security Level:** High (returns sensitive session data)

### 📤 Example Request
```GET /api/v1/active-sessions HTTP/1.1
Host: api.example.com
Authorization: Bearer <your_token>
Accept: application/json
```

### ✅ Successful Response(200 OK)
```{
"sessions": [
{
"session_id": "sess_abc123",
"token": "eyJhbGciOiJI... ", // Показаны первые 10 символов токена с многоточием
"created_at": "2025-06-20T14:30:00Z",
"expires_at": "2025-06-22T18:30:00Z",
"user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
"ip_address": "192.168.1.10"
},
{
"session_id": "sess_xyz789",
"token": "eyJ0eXAiOiJKV1Q... ",
"created_at": "2025-06-21T09:15:00Z",
"expires_at": "2025-06-22T19:15:00Z",
"user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...",
"ip_address": "203.0.113.42"
}
]
}
```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution               |
|-------------|--------------|----------------------------------|---------------------------------|
| `401`       | Unauthorized | Missing or invalid token         | Re-authenticate via /login      |
| `500`       | Server Error | Internal server error            | Retry later or contact support  |


# Accessibility checks

# GET	/check-availability


## GET /check-availability — Check Username Availability

### 🎯 Purpose  
Checks whether a given username is available for registration or already taken by another user.

### 🌐 HTTP Method and URL  
**Method:** `GET`  
**Endpoint:** `/check-availability`  


### 📝 Request Parameters  
| Parameter  | Type   | Required | Description                      |
|------------|--------|----------|--------------------------------|
| `username` | string | Yes      | The username to check availability for |

### 🔐 Authentication  
- **Access:** Public (no authentication required)  
- This endpoint is typically open to allow users to check username availability before registration.

### 📤 Example Request
```GET /api/v1/check-availability?username=fit_user123 HTTP/1.1
Host: api.example.com
Accept: application/json
```

### ✅ Successful Response(200 OK)
```{
"username": "fit_user123",
"available": true
}
```


### ⚠️ Possible Error Responses

| Status Code | Error Type   | Description                      | Typical Resolution                |
|-------------|--------------|----------------------------------|---------------------------------|
| `400`       | Bad Request  | Invalid or missing username parameter | Provide a valid username         |
| `500`       | Server Error | Internal server error             | Retry later or contact support   |


  


