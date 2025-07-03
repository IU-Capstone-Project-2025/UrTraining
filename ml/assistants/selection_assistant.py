import uuid
import typing as tp

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from ml.assistants.utils import format_initial_user_prompt
from ml.assistants.models import SelectionAssistantRequest, SelectionAssistantResponse
from ml.assistants.prompts import SELECTION_ASSISTANT_PROMPT as prompt


class SelectionAssistant:
    def __init__(self, client: OpenAI, model: str) -> None:
        self.client: OpenAI = client
        self.model: str = model
        self.sessions: tp.Dict[uuid.UUID, tp.List[tp.Dict[str, str]]] = {}

    def _get_session(self, session_id: uuid.UUID) -> tp.List[tp.Dict[str, str]]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def chat(self, request: SelectionAssistantRequest) -> SelectionAssistantResponse:
        session: tp.List[tp.Dict[str, str]] = self._get_session(request.session_id)

        # First query in the session
        if not session:
            prompt_with_user_form = prompt.format(
                training_programs="\n".join(request.available_courses),
            )
            session.append({"role": "system", "content": prompt_with_user_form})
            session.append(
                {
                    "role": "user",
                    "content": format_initial_user_prompt(
                        request.query, request.user_form
                    ),
                }
            )
        else:
            session.append(
                {
                    "role": "user",
                    "content": request.query,
                }
            )

        response: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            messages=session,
        )

        session.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content,
            }
        )

        self.sessions[request.session_id] = session  # save session

        return SelectionAssistantResponse(answer=response.choices[0].message.content)
