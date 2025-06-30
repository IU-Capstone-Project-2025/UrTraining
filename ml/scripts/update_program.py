import json
import requests
import os

# Fetch the Kluster API key from the environment variables
KLUSTER_API_KEY = os.environ["KLUSTER_API_KEY"] 

# Define the headers for the API request to Kluster
HEADERS = {
    "Authorization": f"Bearer {KLUSTER_API_KEY}",
    "Content-Type": "application/json"
}


def load_data(path: str = "generated_program.json") -> str:
    """
    Loads a JSON file from the specified path and returns its content as a pretty-printed JSON string.

    Args:
        path (str): The path to the JSON file. Default is 'generated_program.json'.

    Returns:
        str: A formatted JSON string containing the file's contents.
    """
    with open(path, 'r') as f:
        data = json.load(f)
    return json.dumps(data, indent=4)


def update_course_data(program_data_string: str, user_comments: str) -> str:
    """
    Sends a prompt to the Kluster LLM to modify the sport program JSON based on user comments.

    The prompt instructs the model to:
    - Only update fields mentioned in the user comments.
    - Keep all fields from the original JSON schema intact.
    - Return only a single valid JSON object without explanations or markdown.

    Args:
        program_data_string (str): The original or modified JSON sport program as a string.
        user_comments (str): The user's comments describing what needs to be updated.

    Returns:
        str: The updated sport program as a valid JSON string.
    """
    # Define the system prompt with strict formatting and editing instructions
    system_prompt = (
        "You are a JSON data modifier. "
        "Given a starting JSON with a sport program content, you thoroughly analyze the user's "
        "comments and update values of the mentioned in the request fields.\n\n"
        "Strictly follow these rules:\n"
        "- DO NOT OMIT OR SKIP any field from the schema — every field must be included in the final JSON.\n"
        "- Return ONLY a single valid JSON object\n"
        "- DO NOT include markdown, comments, explanations, or natural language.\n\n"
        "- DO NOT MODIFY ANY ADDITIONAL FIELDS: if the field is not listed in comments, return it as it is."
        "Now you are given the following JSON:\n"
    )

    # Construct the full prompt for the user message
    prompt = program_data_string
    prompt += "\nHere are the comments that you must apply:\n"
    prompt += user_comments

    # Define the payload for the API call to Kluster's LLM
    payload = {
        "model": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 3500,
        "temperature": 0.0  # Deterministic output
    }   

    # Send the POST request to the Kluster API
    resp = requests.post("https://api.kluster.ai/v1/chat/completions", headers=HEADERS, json=payload)
    resp.raise_for_status()  # Raise an exception for HTTP errors

    # Extract and return the LLM's response content
    return resp.json()["choices"][0]["message"]["content"].strip()


def main():
    """
    Main interactive loop that:
    - Loads the initial sport program JSON.
    - Allows the user to iteratively submit comments to modify the program.
    - Updates the program using the LLM via the Kluster API.
    - Prints and optionally returns the final modified program.
    """
    # Load the original program data from the file
    program_data_string = load_data()

    # Start an interactive loop for user feedback and modification
    while True:
        print("In case any field is wrong, please put your comments here:\n")
        comments = input(">> ").strip().lower()

        # Pressing "Enter" with no input exits the loop
        if comments == '':
            break

        # Update the program JSON based on user feedback
        program_data_string = update_course_data(program_data_string, comments)

    try:
        # Print the final modified JSON
        print(program_data_string)
        # Attempt to parse and return the valid JSON object
        return json.loads(program_data_string)
    except json.JSONDecodeError:
        # If the LLM's response is not valid JSON, print a warning and raw output
        print("❗ LLM did not return valid JSON. Raw output:")
        print(program_data_string)


# Entry point for script execution
if __name__ == "__main__":
    main()
