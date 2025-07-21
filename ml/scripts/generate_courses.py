import random
import json
import os
from typing import List
from tqdm import tqdm
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODELS: List[str] = [
    "google/gemma-3-27b-it",
    "deepseek-ai/DeepSeek-R1-0528",
    "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
    "Qwen/Qwen3-235B-A22B-FP8"
]
KLUSTER_AI_TOKEN: str = os.getenv("KLUSTER_AI_TOKEN")
NUM_PROGRAMS: int = 100

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key=KLUSTER_AI_TOKEN,
)

# ------------------------- Constants -------------------------

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
    "Course Duration (weeks)": [1, 2, 5],
    "Weekly Training Frequency": ["1-2 times", "3-4 times", "5-6 times"],
    "Average Workout Duration": ["Up to 30 minutes", "30-45 minutes", "45-60 minutes", "More than 60 minutes"],
    "Age Group": ["Teens (13-17)", "Young Adults (18-30)", "Adults (31-50)", "Seniors (51+)", "All Ages"],
    "Gender Orientation": ["For Women", "For Men", "Unisex"],
    "Physical Limitations": ["Joint Issues", "Back Problems", "Post-Injury Recovery", "Pregnancy/Postpartum",
                              "Limited Mobility", "Cardiovascular Diseases", "Diabetes", "Overweight",
                              "Not Adapted (Healthy Only)"],
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

TRAINERS = [
    {"name": "Anna Smirnova", "cert": "ISSA", "level": "Master", "spec": "Yoga", "exp": 8, "courses": 20, "rating": 4.9},
    {"name": "Ivan Orlov", "cert": "ACE", "level": "Advanced", "spec": "Strength Training", "exp": 10, "courses": 15, "rating": 4.8},
    {"name": "Maria Kuznetsova", "cert": "NASM", "level": "Basic", "spec": "Pilates", "exp": 5, "courses": 10, "rating": 4.7}
]

# ------------------------- Helper Functions -------------------------

def random_multichoice(options, min_count=1, max_count=4):
    return random.sample(options, k=random.randint(min_count, min(max_count, len(options))))

def generate_metadata():
    trainer = random.choice(TRAINERS)
    metadata = {
        "Activity Type": random.choice(CATEGORIES["Activity Type"]),
        "Program Goal": random.sample(CATEGORIES["Program Goal"], k=random.randint(1, 2)),
        "Training Environment": random_multichoice(CATEGORIES["Training Environment"], 1, 3),
        "Difficulty Level": random.choice(CATEGORIES["Difficulty Level"]),
        "Course Duration (weeks)": random.choice(CATEGORIES["Course Duration (weeks)"]),
        "Weekly Training Frequency": random.choice(CATEGORIES["Weekly Training Frequency"]),
        "Average Workout Duration": random.choice(CATEGORIES["Average Workout Duration"]),
        "Age Group": random_multichoice(CATEGORIES["Age Group"], 1, 3),
        "Gender Orientation": random.choice(CATEGORIES["Gender Orientation"]),
        "Physical Limitations": random_multichoice(CATEGORIES["Physical Limitations"], 0, 3),
        "Required Equipment": random_multichoice(CATEGORIES["Required Equipment"], 1, 3),
        "Course Language": random.choice(CATEGORIES["Course Language"]),
        "Visual Content": random_multichoice(CATEGORIES["Visual Content"], 1, 2),
        "Trainer Feedback Options": random_multichoice(CATEGORIES["Trainer Feedback Options"], 0, 3),
        "Tags": random.sample(CATEGORIES["Tags"], k=random.randint(3, 10)),
        "Average Course Rating": round(random.uniform(3.5, 5.0), 2),
        "Active Participants": random.randint(10, 1000),
        "Number of Reviews": random.randint(0, 500),
        "Certification": {
            "Type": trainer["cert"],
            "Level": trainer["level"],
            "Specialization": trainer["spec"]
        },
        "Experience": {
            "Years": trainer["exp"],
            "Specialization": trainer["spec"],
            "Courses": trainer["courses"],
            "Rating": trainer["rating"]
        },
        "Trainer Name": trainer["name"]
    }
    return metadata

def generate_prompt(metadata):
    return f"""Generate a structured workout program plan for {metadata['Course Duration (weeks)']} weeks based on the following information:
- Activity Type: {metadata['Activity Type']}
- Goal: {', '.join(metadata['Program Goal'])}
- Level: {metadata['Difficulty Level']}
- Avg Duration: {metadata['Average Workout Duration']}
- Frequency: {metadata['Weekly Training Frequency']} per week
- Trainer: {metadata['Trainer Name']} ({metadata['Certification']['Type']}, {metadata['Certification']['Level']})

Provide a daily schedule with:
- Exercise names
- Repetitions or sets
- Rest time
- Additional recommendations (e.g., warm-up, supplements, hydration)"""

system_prompt = """
You are a professional fitness coach and healthy lifestyle expert. Your task is to create effective, diverse, and motivating fitness programs tailored to users with various goals, skill levels, and preferences. You take into account the user's goals (e.g., weight loss, muscle gain, endurance), available equipment, training frequency, and individual characteristics. Respond with a structured and detailed fitness program. Your program must be useful, realistic, and inspiring.
"""

def call_llm(model_id, prompt):
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model=model_id, messages=messages, temperature=0.1, top_p=0.9
    )
    return response.choices[0].message.content

# ------------------------- Main Generation Loop -------------------------

for model_id in MODELS:
    data = []

    for _ in tqdm(range(NUM_PROGRAMS), desc=f"Generating courses by {model_id}"):
        meta = generate_metadata()
        meta["Course Title"] = f"{random.choice(meta['Program Goal'])} with {meta['Trainer Name']}"
        prompt = generate_prompt(meta)
        try:
            description = call_llm(model_id, prompt)
        except Exception as e:
            description = f"Error: {e}"
        meta["Program Description"] = description
        data.append(meta)

    with open(f"{NUM_PROGRAMS}_sport_programs_{model_id}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"{NUM_PROGRAMS} {model_id} programs generated and saved.")