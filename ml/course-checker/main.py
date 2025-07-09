from fastapi import FastAPI, HTTPException
import json

from utils import call_kluster_llm
from models import TrainingUpdate, ValidationResponse, EditRequest, EditResponse


app = FastAPI(
    title="Sport Training Program Assistant API",
    description=(
        "API to validate and edit sport training program data using a Kluster LLM assistant. "
        "Two modes:\n"
        "1. Validation mode: Check completeness and correctness of training JSON, return feedback or confirmation.\n"
        "2. Editing mode: Modify training JSON based on user instructions.\n"
        "Requires KLUSTER_API_KEY in environment."
    ),
    version="1.0"
)


# === Endpoint 1: Validate training program data ===

@app.post("/validate-training/", response_model=ValidationResponse, summary="Validate training program completeness and correctness")
def validate_training(training: TrainingUpdate):
    """
    Validate the completeness and correctness of a training program JSON structure.

    The LLM assistant receives the training data and:
    - Checks if all required fields are filled.
    - Checks if values are plausible and within expected ranges.
    - Returns either a success message or a list of structured requests to improve the data.

    Returns a JSON with status 'ok' or 'needs_correction' and detailed requests.
    """
    system_prompt = (
        "You are a sport training program validation assistant.\n"
        "You receive a JSON structure of a training program. Your task is to check if all required fields are properly filled, "
        "and if the values are valid and plausible according to the schema and domain knowledge.\n\n"
        "You have an example of a correct training program structure and rules to judge validity.\n\n"
        "If everything is filled correctly, respond with a single JSON object:\n"
        '{"status":"ok","message":"Great job! All required fields are correctly filled. Thank you!"}\n\n'
        "If there are missing or invalid fields, respond with a JSON object:\n"
        '{"status":"needs_correction","requests":[list_of_requests_strings]}\n'
        "Each request should be a short message clearly indicating the field and what is missing or wrong, e.g.:\n"
        '"Age group: Please add valid age information."\n'
        '"Required equipment: Add missing equipment details."\n'
        '"Age group: Invalid age range detected (123 years)."\n\n'
        "Respond ONLY with the JSON object, no explanations or markdown."
    )

    user_message = training.json()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    llm_response = call_kluster_llm(
        model="klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        temperature=0.0
    )

    try:
        print(llm_response)
        # Parse LLM JSON response
        result = json.loads(llm_response)
        # Validate keys in result
        if "status" not in result:
            raise ValueError("Missing 'status' key")
        if result["status"] == "needs_correction" and "requests" not in result:
            raise ValueError("Missing 'requests' key when status is 'needs_correction'")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON response from LLM: {e}\nResponse: {llm_response}")

# === Endpoint 2: Edit training program data ===

@app.post("/edit-training/", response_model=EditResponse, summary="Edit training program based on user prompt")
def edit_training(edit_req: EditRequest):
    """
    Edit the sport training program JSON based on user instructions.

    The assistant receives the original training program JSON plus user comments specifying desired modifications.
    It updates only the fields mentioned, preserving the rest exactly.

    Returns the updated training program JSON.
    """
    system_prompt = (
        "You are a JSON data modifier specialized in sport training programs.\n"
        "Given an input JSON with a training program and a user's editing instructions, you must:\n"
        "- Only update fields explicitly mentioned in the user's instructions.\n"
        "- Keep all other fields unchanged.\n"
        "- Return ONLY a single valid JSON object without markdown or comments.\n"
        "- Do NOT omit any fields from the original JSON schema.\n"
        "- Ensure you made ALL THE NEEDED CHANGES.\n\n"
        "Input JSON:"
    )

    program_json_str = edit_req.training_data.json()
    user_content = program_json_str + "\nUser instructions:\n" + edit_req.user_prompt

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

    llm_response = call_kluster_llm(
        model="klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=messages,
        temperature=0.0
    )

    try:
        updated_data = json.loads(llm_response)
        return {"updated_training_data": updated_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Invalid JSON response from LLM: {e}\nResponse: {llm_response}")

@app.get("/", summary="Root endpoint")
def read_root():
    return {"message": "Sport Training Program Assistant is running."}