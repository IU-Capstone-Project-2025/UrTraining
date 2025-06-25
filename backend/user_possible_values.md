# User Core Data Specifications

## 1. `full_name`
**Type:** `string`  
**Validation Rules:**
- Minimum length: 2 characters
- Maximum length: 100 characters

## 2. `email`  
**Type:** `string`  
**Validation Rules:**
- Required: Yes
- Format: Valid email
- Unique: Yes (system-wide)

## 3. `username`  
**Type:** `string`  
**Validation Rules:**
- Required: Yes
- Minimum length: 3 characters
- Maximum length: 50 characters
- Unique: Yes (system-wide)
# Training Profile

## 2.1 Basic Information

| Field      | Type    | Allowed Values                  | Constraints               |
|------------|---------|--------------------------------|--------------------------|
| **gender** | string  | `"male"`, `"female"`            |                          |
| **age**    | integer |                                | Minimum: 13, Maximum: 100 |
| **height_cm** | integer |                             | Minimum: 100, Maximum: 250 |
| **weight_kg** | float  |                              | Minimum: 30.0, Maximum: 300.0 |

---

## 2.2 Training Goals

| Field           | Type  | Allowed Values                                                                                   | Constraints            |
|-----------------|-------|-------------------------------------------------------------------------------------------------|-----------------------|
| **training_goals** | array | `"muscle_gain"`, `"maintain_fitness"`, `"weight_loss"`, `"improve_endurance"`, `"improve_flexibility"`, `"stress_reduction"`, `"competitions_preparation"`, `"none"` | Maximum number of elements: 2 |

---

## 2.3 Training Experience

| Field                | Type   | Allowed Values                                      |
|----------------------|--------|----------------------------------------------------|
| **level**            | string | `"beginner"`, `"intermediate"`, `"advanced"`       |
| **frequency_last_3_months** | string | `"1_2_times_week"`, `"3_4_times_week"`, `"5+_times_week"`, `"not_trained"` |

---

## 2.4 Preferences

| Field             | Type   | Allowed Values                                                                                   |
|-------------------|--------|-------------------------------------------------------------------------------------------------|
| **training_location** | string | `"gym"`, `"outdoors"`, `"pool"`, `"home"`                                                     |
| **location_details**  | string | `"full_equipment"`, `"basic_equipment"`, `"no_equipment"`, `"outdoor_park"`, `"running_track"`, `"swimming_pool"`, `"home_gym"`, `"bodyweight_only"` |
| **session_duration**  | string | `"under_30_min"`, `"30_45_min"`, `"45_60_min"`, `"over_60_min"`                               |

---

## 2.5 Health

| Field               | Type    | Allowed Values          | Constraints             |
|---------------------|---------|------------------------|------------------------|
| **joint_back_problems** | boolean | `true`, `false`         |                        |
| **chronic_conditions**  | boolean | `true`, `false`         |                        |
| **health_details**      | string  |                        | Optional (nullable), Max length: 1000 |

---

## 2.6 Training Types

All fields are integers on a scale from 1 to 5.

| Field               | Type    | Constraints        |
|---------------------|---------|--------------------|
| **strength_training** | integer | Minimum: 1, Maximum: 5 |
| **cardio**            | integer | Minimum: 1, Maximum: 5 |
| **hiit**              | integer | Minimum: 1, Maximum: 5 |
| **yoga_pilates**      | integer | Minimum: 1, Maximum: 5 |
| **functional_training**| integer | Minimum: 1, Maximum: 5 |
| **stretching**        | integer | Minimum: 1, Maximum: 5 |

---
## 3. Countries

Allowed values include the following country objects:

- `{ "code": "kz", "name": "kazakhstan", "display_name": "Kazakhstan" }`
- `{ "code": "ru", "name": "russia", "display_name": "Russia" }`
- `{ "code": "us", "name": "usa", "display_name": "United States" }`

---

## 4. General Validation Rules

### Required Fields
- `user_data.full_name`
- `user_data.email`
- `user_data.username`

### Unique Fields
- `user_data.email`
- `user_data.username`

### Numeric Ranges
- `age`: 13 to 100
- `height_cm`: 100 to 250
- `weight_kg`: 30.0 to 300.0
- `training_interest_scale`: 1 to 5

### String Length Limits
- `username`: 3 to 50 characters
- `full_name`: 2 to 100 characters
- `health_details`: maximum 1000 characters

# Default Values for User Profile

## Main Purpose  
When a user does not provide certain data in their profile, the system will automatically fill in these predefined default values.

---

## Data Structure

### Basic Information (basic_information):
- Gender: male (`"male"`)
- Age: 25 years
- Height: 170 cm
- Weight: 70 kg

### Training Goals:
- Default: maintain fitness (`"maintain_fitness"`)

### Training Experience:
- Level: beginner (`"beginner"`)
- Frequency: 1-2 times per week

### Preferences:
- Training location: home
- Equipment: none
- Session duration: 30-45 minutes

### Health:
- No joint or back problems
- No chronic conditions
- Additional health details: not specified

### Training Types (scale 1-5):
- Strength training: 3
- Cardio: 3
- HIIT: 2
- Yoga/Pilates: 2
- Functional training: 3
- Stretching: 4
