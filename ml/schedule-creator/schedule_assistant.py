from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion
import logging
from typing import List, Dict, Any
import re, json

from models import TrackerAssistantRequest, TrackerAssistantResponse
from prompts import TRACKER_ASSISTANT_PROMPT

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TrackerAssistant:
    def __init__(self, client: AsyncOpenAI, model: str) -> None:
        self.client = client
        self.model = model

    def _format_data(self, training_plan: list, training_profile: dict, start_date: str) -> str:
        return f"""
**Training Plan:**
{training_plan}

**Training Profile:**
{training_profile}

**Start Date:**
{start_date}
""".strip()

    async def generate(self, request: TrackerAssistantRequest) -> TrackerAssistantResponse:

        logger.info(f"Request: {request}")

        formatted_input = self._format_data(
            request.training_plan, request.training_profile, request.start_date
        )

        logger.info(f"Formatted input: {formatted_input}")

        try:
            prompt = TRACKER_ASSISTANT_PROMPT.format(course_data=formatted_input)
            logger.info(f"Prompt: {prompt}")
        except Exception as e:
            logger.exception("Failed to format prompt")
            raise

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze the training plan and user preferences data, and create a training schedule based on what you analyzed."
                        ),
                    },
                ],
            },
        ]

        response: ChatCompletion = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.0
        )

        content = response.choices[0].message.content.strip()
        logger.info(f"Generated content: {content}")
        parsed_content = self.extract_json_from_response(content)

        return TrackerAssistantResponse(schedule=parsed_content)
    
    
    def extract_json_from_response(self, response: str) -> list[dict]:

        match = re.search(r"```json\s*(.*?)```", response, re.DOTALL)
        json_str = match.group(1).strip() if match else response.strip()
        
        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON: {e}")
            return []
        

