CLIENT_FORM_SYNT_DATA_PROMPT = """I'm working on a fitness application called UrTraining and need to generate synthetic client questionnaire data for testing purposes.

Please create a realistic client questionnaire in JSON format. Generate plausible user data (name, age, gender, height, weight, goals, training experience, etc.) that could belong to a real person.

The JSON structure should strictly follow these fields from our questionnaire:

1. Personal data:
   - full_name (string)

2. Basic information:
   - gender (string: "male" or "female")
   - age (number)
   - height_cm (number)
   - weight_kg (number)

3. Training goals (array with up to 2 items from):
   - "weight_loss"
   - "muscle_gain"
   - "improve_endurance"
   - "improve_flexibility"
   - "maintain_fitness"
   - "competition_preparation"
   - "stress_reduction"

4. Training experience:
   - level (string: "beginner", "intermediate", or "advanced")
   - frequency_last_3_months (string: "not_trained", "1_2_times_month", "1_2_times_week", "3_4_times_week", "5+_times_week")

5. Preferences:
   - training_location (string: "gym", "home", "pool", "outdoors")
   - location_details (string, must match the training_location):
     * For "gym": "full_fitness_center" or "small_gym_basic_equipment"
     * For "home": "some_equipment" or "bodyweight_only"
     * For "pool": null
     * For "outdoors": "sports_ground" or "park_no_equipment"
   - session_duration (string: "under_30_min", "30_45_min", "45_60_min", "over_60_min")

6. Health:
   - joint_back_problems (boolean)
   - chronic_conditions (boolean)
   - health_details (string or null if both above are false)

7. Training types (rating from 1 to 5 for each):
   - strength_training (number)
   - cardio (number)
   - hiit (number)
   - yoga_pilates (number)
   - functional_training (number)
   - stretching (number)

Make sure the data is consistent (e.g., goals should align with preferred training types). Create a realistic profile for this user.

Return ONLY a valid JSON object without any additional text.

Example output format:
{
  "personal_data": {
    "full_name": "Maria Ivanova"
  },
  "basic_information": {
    "gender": "female",
    "age": 28,
    "height_cm": 165,
    "weight_kg": 62,
  },
  "training_goals": [
    "weight_loss",
    "improve_flexibility"
  ],
  "training_experience": {
    "level": "intermediate",
    "frequency_last_3_months": "1_2_times_week"
  },
  "preferences": {
    "training_location": "gym",
    "location_details": "full_fitness_center",
    "session_duration": "45_60_min"
  },
  "health": {
    "joint_back_problems": false,
    "chronic_conditions": false,
    "health_details": null
  },
  "training_types": {
    "strength_training": 3,
    "cardio": 4,
    "hiit": 4,
    "yoga_pilates": 5,
    "functional_training": 2,
    "stretching": 5
  }
}
"""