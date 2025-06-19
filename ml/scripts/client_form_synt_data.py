"""
Commands:
python client_form_synt_data.py -n 10 -m gemma -t 0.9 -o gemma_profiles.json -b 5
python client_form_synt_data.py -n 10 -m deepseek_r1 -t 0.8 -o deepseek_profiles.json -b 5
python client_form_synt_data.py -n 10 -m llama3.1_8b -t 0.8 -o llama_profiles.json -b 5
python client_form_synt_data.py -n 10 -m qwen235b -t 0.8 -o qwen_profiles.json -b 5
"""

import os
import json
import argparse
import random
import time
from tqdm import tqdm
from dotenv import load_dotenv
from typing import Dict, Optional, List
from concurrent.futures import ThreadPoolExecutor, as_completed

from prompts import CLIENT_FORM_SYNT_DATA_PROMPT as prefix

from openai import OpenAI
from openai.types.chat import ChatCompletion

load_dotenv()

KLUSTER_AI_TOKEN: str = os.getenv("KLUSTER_AI_TOKEN")
MODELS: Dict[str, str] = {
    "gemma": "google/gemma-3-27b-it",
    "deepseek_r1": "deepseek-ai/DeepSeek-R1-0528",
    "llama3.1_8b": "klusterai/Meta-Llama-3.1-8B-Instruct-Turbo",
    "qwen235b": "Qwen/Qwen3-235B-A22B-FP8",
}
client = OpenAI(
    base_url="https://api.kluster.ai/v1",
    api_key=KLUSTER_AI_TOKEN,
)


def get_response(
    model_name: str,
    user_prompt: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = 0.25,
    top_p: Optional[float] = 0.9,
) -> ChatCompletion:
    model_id: str = MODELS.get(model_name, None)
    assert (
        model_id is not None
    ), f"Model type '{model_name}' is not supported. List of supported models: {MODELS.keys()}"

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    messages.append({"role": "user", "content": user_prompt})

    response = client.chat.completions.create(
        model=model_id, messages=messages, temperature=temperature, top_p=top_p
    )

    return response


def extract_thinking(raw_answer: str) -> str:
    thinking_idx: int = raw_answer.find("</think>")
    if thinking_idx == -1:
        return ""

    thinking: str = raw_answer[:thinking_idx].strip()
    return thinking


def extract_regular_content(raw_answer: str) -> str:
    thinking_end_idx = raw_answer.find("</think>")

    if thinking_end_idx == -1:
        return raw_answer.strip()

    regular_content: str = raw_answer[thinking_end_idx + len("</think>") :].strip()
    return regular_content


def generate_single_profile(
    model_name: str, temperature: float, seed: int = 1337
) -> str:
    """
    Generate a single synthetic profile
    """
    response: ChatCompletion = get_response(
        model_name=model_name,
        user_prompt=get_prompt_with_seed(seed),
        temperature=temperature,
    )
    content: str = response.choices[0].message.content
    return extract_regular_content(content)


def try_parse_json(content: str) -> Optional[Dict]:
    try:
        content = content.replace("```json", "")
        content = content.replace("```", "")
        return json.loads(content)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None


def get_prompt_with_seed(seed_number: int):
    """Generate a prompt with a random seed to ensure variety in outputs"""

    random.seed(seed_number)
    gender_options = [
        {"gender": "male", "letters": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
        {"gender": "female", "letters": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"},
    ]

    # Select gender
    gender_option = random.choice(gender_options)
    chosen_gender = gender_option["gender"]
    first_letter = random.choice(gender_option["letters"])

    age_ranges = [
        "in their early 20s",
        "in their late 20s",
        "in their early 30s",
        "in their late 30s",
        "in their 40s",
        "in their 50s",
        "in their 60s",
    ]
    chosen_age = random.choice(age_ranges)

    characteristics = [
        "a busy professional",
        "a college student",
        "a parent",
        "a retiree",
        "an athlete",
        "a beginner in fitness",
        "someone recovering from injury",
        "a digital nomad",
        "an office worker",
        "a fitness enthusiast",
    ]

    locations = [
        "from New York",
        "from California",
        "from Russia",
        "from London",
        "from Paris",
        "from Tokyo",
        "from Moscow",
        "from Sydney",
        "from Berlin",
        "from a small town",
        "from a big city",
    ]

    backgrounds = [
        "who recently decided to get in shape",
        "who has been trying different workout routines",
        "who wants to improve their overall health",
        "who is training for a specific event",
        "who is coming back to fitness after a break",
        "who needs a structured training plan",
        "who wants to maintain their current fitness level",
        "who is looking for variety in their workouts",
    ]

    body_types = [
        "with a slim build",
        "with an athletic build",
        "with a muscular build",
        "with a stocky build",
        "with a lean build",
        "with an average build",
        "",
    ]
    chosen_body = random.choice(body_types)
    characteristic = random.choice(characteristics)
    location = random.choice(locations)
    background = random.choice(backgrounds)

    # Construct the seed phrase
    seed_text = (
        f"\nFor this profile, create a {chosen_gender} {chosen_age} {characteristic} {location} {background} {chosen_body}. "
        f"The person's name should start with the letter '{first_letter}'. "
        f"Make sure the profile details are realistic and consistent with this background."
    )

    full_prompt = prefix + seed_text

    return full_prompt


def generate_profiles(
    model_name: str,
    count: int,
    output_file: str,
    batch_size: int = 5,
    temperature: float = 0.7,
    timeout: int = 600,
) -> None:
    """
    Generate multiple synthetic profiles in batches

    Args:
        model_name: Model to use for generation
        count: Number of profiles to generate
        output_file: File to save the profiles to
        batch_size: Number of profiles to generate in parallel
        temperature: Temperature for generation diversity
        timeout: Maximum time (in seconds) to wait for a batch
    """
    profiles = []
    start_time = time.time()

    # Function to process a single batch
    def process_batch(batch_idx: int, size: int) -> List[Dict]:
        batch_results = []
        seed_base: int = 42
        with ThreadPoolExecutor(max_workers=size) as executor:
            futures = {
                executor.submit(
                    generate_single_profile,
                    model_name,
                    temperature,
                    seed_base + batch_idx * size + i,
                ): i
                for i in range(size)
            }

            for future in as_completed(futures):
                try:
                    content = future.result()
                    profile = try_parse_json(content)
                    if profile:
                        batch_results.append(profile)
                    else:
                        print(f"Failed to parse profile in batch {batch_idx}")
                except Exception as e:
                    print(f"Error generating profile: {e}")

        return batch_results

    with tqdm(total=count, desc="Generating profiles...") as pbar:
        for i in range(0, count, batch_size):
            current_batch_size = min(batch_size, count - i)

            batch_start_time = time.time()
            batch_profiles = process_batch(i // batch_size + 1, current_batch_size)

            profiles.extend(batch_profiles)
            pbar.update(len(batch_profiles))

    with open(output_file, "w") as file:
        file.write(json.dumps(profiles, ensure_ascii=False, indent=2))

    print(
        f"Generated {len(profiles)} profiles in {time.time() - start_time:.2f} seconds"
    )
    print(f"Results saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic client profiles")

    parser.add_argument(
        "-n", "--count", type=int, required=True, help="Number of profiles to generate"
    )

    parser.add_argument(
        "-m",
        "--model",
        type=str,
        default="deepseek_r1",
        choices=list(MODELS.keys()),
        help=f"Model to use for generation. Available models: {', '.join(MODELS.keys())}",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="synthetic_profiles.json",
        help="Output file to save the profiles to",
    )
    parser.add_argument(
        "-b",
        "--batch-size",
        type=int,
        default=5,
        help="Number of profiles to generate in parallel",
    )
    parser.add_argument(
        "-t",
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for generation diversity (0.0-1.0)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Maximum time (in seconds) to wait for generation",
    )

    args = parser.parse_args()

    if args.count <= 0:
        parser.error("Count must be a positive integer")

    if args.batch_size <= 0:
        parser.error("Batch size must be a positive integer")

    if not (0.0 <= args.temperature <= 1.0):
        parser.error("Temperature must be between 0.0 and 1.0")

    generate_profiles(
        model_name=args.model,
        count=args.count,
        output_file=args.output,
        batch_size=args.batch_size,
        temperature=args.temperature,
        timeout=args.timeout,
    )


if __name__ == "__main__":
    main()
