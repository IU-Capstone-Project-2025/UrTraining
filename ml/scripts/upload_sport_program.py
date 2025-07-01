#!/usr/bin/env python3
"""
upload_pipeline.py

End‑to‑end: image/text → OCR → LLM form fill → missing‑field prompts → final dict.

Fields:
  - 16 categoricals with fixed allowed values (see CATEGORIES dict).
  - "Program Description": day-by-day structured workout plan.

Output: single Python dict mapping each field to its chosen/value.
"""

import os
import sys
import json
import requests

# ─── Configuration ─────────────────────────────────────────────────────────────

KLUSTER_API_KEY = os.environ["KLUSTER_API_KEY"] 
if not KLUSTER_API_KEY:
    print("❗ Please set your KLUSTER_API_KEY environment variable.")
    sys.exit(1)

HEADERS = {
    "Authorization": f"Bearer {KLUSTER_API_KEY}",
    "Content-Type": "application/json"
}

# ─── Field Definitions ──────────────────────────────────────────────────────────

CATEGORIES = {
    "Activity Type": ["Strength Training", "Cardio", "HIIT", "Yoga", "Pilates", "Functional Training",
                      "CrossFit", "Bodybuilding", "Stretching", "Running", "Swimming", "Cycling",
                      "Boxing/Martial Arts", "Dancing"],
    "Program Goal": ["Weight Loss", "Muscle Gain", "Endurance Improvement", "Flexibility Improvement",
                     "Maintaining Fitness", "Competition Preparation", "Rehabilitation", "Stress Relief",
                     "Health Improvement"],
    "Training Environment": ["Home Without Equipment", "Home With Basic Equipment", "Gym",
                             "Outdoors", "Pool", "Universal"],
    "Difficulty Level": ["Beginner", "Intermediate", "Advanced", "All Levels (Adaptive Program)"],
    "Course Duration (weeks)": [2, 5, 10],
    "Weekly Training Frequency": ["1-2 times", "3-4 times", "5-6 times"],
    "Average Workout Duration": ["Up to 30 minutes", "30-45 minutes", "45-60 minutes", "More than 60 minutes"],
    "Age Group": ["Teens (13-17)", "Young Adults (18-30)", "Adults (31-50)", "Seniors (51+)", "All Ages"],
    "Gender Orientation": ["For Women", "For Men", "Unisex"],
    "Physical Limitations": ["Joint Issues", "Back Problems", "Post-Injury Recovery",
                              "Pregnancy/Postpartum", "Limited Mobility", "Cardiovascular Diseases",
                              "Diabetes", "Overweight", "Not Adapted (Healthy Only)"],
    "Required Equipment": ["No Equipment", "Fitness Mat", "Dumbbells", "Barbell and Plates", "Gym Machines",
                           "Pull-up/Dip Bars", "Resistance Bands", "Jump Rope", "Fitball", "TRX/Suspension Trainer",
                           "Step Platform", "Boxing Bag", "Specific Equipment (specify)"],
    "Course Language": ["English", "Other"],
    "Visual Content": ["Exercise Photos", "Video Demonstrations", "Technique Animations",
                       "Progress Graphs", "Minimal Visual Content"],
    "Trainer Feedback Options": ["Lesson Comments", "Personal Consultations", "Group Online Sessions",
                                 "Support Chat", "No Feedback"],
    "Tags": ["Weight Loss", "Muscle Gain", "Strength", "Endurance", "Flexibility", "Balance", "Coordination",
             "Speed", "Rehabilitation", "Posture", "Abs", "Glutes", "Arms", "Legs", "Back", "Explosive Strength",
             "Mobility", "Beach Body", "High Intensity", "Low Intensity", "No Jumps", "Knee Safe",
             "Short Workouts", "Morning Workouts", "Recovery", "For Beginners", "For Experienced",
             "No Equipment", "Minimal Equipment", "Marathon Prep", "Functionality", "Injury Prevention",
             "Sports Performance", "Home Workouts", "Fat Burning", "Active Longevity", "Anti-Stress",
             "Energy", "Better Sleep", "Metabolism"]
}

ALL_FIELDS = list(CATEGORIES.keys()) + ["Program Description"]


# ─── Helper Functions ──────────────────────────────────────────────────────────

def extract_text_from_image(image_path: str) -> str:
    """
    Sends an image to kluster.ai chat completion with vision-capable model
    to extract text as output.
    """
    import base64
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "model": "google/gemma-3-27b-it",
        "messages": [
            {"role": "system", "content": "You are an OCR assistant. Extract all text from the image."},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please extract all text from the following image."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 1500,
        "temperature": 0
    }
    resp = requests.post("https://api.kluster.ai/v1/chat/completions", headers=HEADERS, json=payload)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()

def fill_form_with_llm(raw_text: str) -> dict:
    """
    Send raw_text + field specs to LLM, asking it to choose/produce values.
    If info is missing, model must ask follow‑up questions.
    Expects pure JSON response mapping fields→values.
    """
    spec = {
        field: CATEGORIES[field] if field in CATEGORIES else "Structured day-by-day plan text"
        for field in ALL_FIELDS
    }
    prompt = (
        "You are a JSON data extractor and generator.\n\n"
        "Your task is to fill **ALL fields** in a structured JSON object that represents a training program.\n\n"
        "Below is a list of required fields and their allowed values:\n"
        f"{json.dumps(spec, ensure_ascii=False, indent=2)}\n\n"
        "Special rules:\n"
        "- DO NOT OMIT OR SKIP any field from the schema — every field must be included in the final JSON.\n"
        "- If some information is missing from the input, **guess logically** based on context or defaults.\n"
        "- For `Program Description`: YOU MUST GENERATE a detailed multi-week training plan based on the input.\n"
        "- The plan must be structured by day and include:\n"
        "  - Specific exercises\n"
        "  - Number of sets, reps, rounds, or duration\n"
        "  - Only real training data (NO metadata or tags inside the description)\n"
        "- Use full day names (e.g., \"Monday\", \"Tuesday\", etc.) as keys.\n"
        "- Use a nested structure: `\"Program Description\": {\"Week 1\": {\"Monday\": [\"...\"], ...}, ...}`\n"
        "- The plan should match the total course duration (in weeks) and frequency fields.\n\n"
        "Output rules:\n"
        "- Return ONLY a single valid JSON object\n"
        "- DO NOT include markdown, comments, explanations, or natural language.\n"
        "- Use word abbreviations to make the answer shorter (e.g. minutes -> min.).\n"
        "- Ensure the output conforms strictly to this schema:\n"
        "{\n"
        "  \"Activity Type\": \"...\",\n"
        "  \"Program Goal\": \"...\",\n"
        "  \"Training Environment\": \"...\",\n"
        "  \"Difficulty Level\": \"...\",\n"
        "  \"Course Duration (weeks)\": ...,\n"
        "  \"Weekly Training Frequency\": \"...\",\n"
        "  \"Average Workout Duration\": \"...\",\n"
        "  \"Age Group\": \"...\",\n"
        "  \"Gender Orientation\": \"...\",\n"
        "  \"Physical Limitations\": \"...\",\n"
        "  \"Required Equipment\": \"...\",\n"
        "  \"Course Language\": \"...\",\n"
        "  \"Visual Content\": \"...\",\n"
        "  \"Trainer Feedback Options\": \"...\",\n"
        "  \"Tags\": [\"...\"],\n"
        "  \"Program Description\": {\n"
        "    \"Week 1\": {\n"
        "      \"Monday\": [\"Exercise 1\", \"Exercise 2\", ...],\n"
        "      ...\n"
        "    },\n"
        "    ...\n"
        "  }\n"
        "}\n\n"
        "=== PROGRAM RAW TEXT START ===\n"
        f"{raw_text.strip()}\n"
        "=== PROGRAM RAW TEXT END ===\n"
    )

    headers = {
        "Authorization": f"Bearer {KLUSTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",  # valid Kluster model
        "messages": [
            {"role": "system", "content": "You are a form-filling assistant."},
            {"role": "user", "content": prompt}
        ],
    "max_tokens": 3500,
    "temperature": 0.0
}   
    resp = requests.post("https://api.kluster.ai/v1/chat/completions", headers=headers, json=payload)
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"].strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("❗ LLM did not return valid JSON. Raw output:")
        print(text)

def prompt_missing_fields(data: dict) -> dict:
    """Interactively ask coach to supply any field still empty or null."""
    for field in ALL_FIELDS:
        if field not in data or data[field] in (None, "", []):
            data[field] = input(f"Please provide a value for '{field}': ").strip()
    return data


# ─── Main Pipeline ────────────────────────────────────────────────────────────

def main():
    print("Mode: 'image' to upload sketch, 'text' to paste program text.")
    mode = input(">> ").strip().lower()

    if mode == "image":
        path = input("Path to image file: ").strip()
        raw = extract_text_from_image(path)
        print("\nExtracted text:\n", raw, "\n")
    elif mode == "text":
        path = input("Path to text file: ").strip()
        with open(path, 'r') as f:
            raw = f.read()
    else:
        print("Invalid mode. Exiting."); sys.exit(1)

    # 1) LLM fills form
    filled = fill_form_with_llm(raw)

    # 2) Ask for any missing pieces
    filled = prompt_missing_fields(filled)

    # 3) Show final dict
    print("\n✅ Final program dict:")
    print(json.dumps(filled, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
