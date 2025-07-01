import os
from typing import List, Dict, Any

import fastapi
import uvicorn
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from schema import Image2TrackerRequest, Image2TrackerResponse
from prompts import IMAGE_TO_TRAINING_PLAN_PROMPT


MODEL_ID = os.getenv("MODEL_ID", "google/gemma-3-27b-it")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = fastapi.FastAPI()


@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "image2tracker"}


def postprocess_response(response: str) -> str:
    response = response.replace("```json", "").replace("```", "")
    return response


@app.post("/image2tracker")
async def image2tracker(request: Image2TrackerRequest) -> Image2TrackerResponse:
    try:
        client = OpenAI(
            api_key=OPENAI_API_KEY, 
            base_url="https://api.kluster.ai/v1"
        )
        image_base64 = request.image

        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": IMAGE_TO_TRAINING_PLAN_PROMPT},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            request.query
                            if request.query
                            else "Analyze this fitness image and create a training plan based on what you see."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"},
                    },
                ],
            },
        ]

        response: ChatCompletion = client.chat.completions.create(
            model=MODEL_ID, messages=messages, max_tokens=2000, temperature=0.0
        )

        answer: str = postprocess_response(response.choices[0].message.content)

        return Image2TrackerResponse(response=answer)
    
    except Exception as e:
        print(f"Error in image2tracker: {str(e)}")
        return Image2TrackerResponse(response=f"Error processing request: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
