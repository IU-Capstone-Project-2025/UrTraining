import uuid
import typing as tp
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from util import format_initial_user_prompt
from models import CourseAssistantRequest, CourseAssistantResponse
from prompts import COURSE_ASSISTANT_PROMPT as prompt

class CourseAssistant:
    def __init__(self, client: AsyncOpenAI, model: str) -> None:
        self.client: AsyncOpenAI = client
        self.model: str = model
        self.sessions: tp.Dict[uuid.UUID, tp.List[tp.Dict[str, str]]] = {}

    def _get_session(self, session_id: uuid.UUID) -> tp.List[tp.Dict[str, str]]:
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def _format_course_data(self, course_data: dict) -> str:
        """Formats course data into readable text"""
        formatted = f"""
**Basic information:**
- Course name: {course_data.get('Course Title', 'N/A')}
- Type of activity: {course_data.get('Activity Type', 'N/A')}
- Coach: {course_data.get('Trainer Name', 'N/A')}
- Language of the course: {course_data.get('Course Language', 'N/A')}

**Program Details:**
- Difficulty level: {course_data.get('Difficulty Level', 'N/A')}
- Duration: {course_data.get('Course Duration (weeks)', 'N/A')} weeks
- Training frequency: {course_data.get('Weekly Training Frequency', 'N/A')}
- Average training duration:{course_data.get('Average Workout Duration', 'N/A')}
- Objectives of the program: {', '.join(course_data.get('Program Goal', [])) or 'N/A'}
- Training environment: {', '.join(course_data.get('Training Environment', [])) or 'N/A'}
- Age group: {', '.join(course_data.get('Age Group', [])) or 'N/A'}
- Gender orientation: {course_data.get('Gender Orientation', 'N/A')}
- Physical limitations: {', '.join(course_data.get('Physical Limitations', [])) or 'Нет'}
- Necessary equipment: {', '.join(course_data.get('Required Equipment', [])) or 'N/A'}

**Ratings and statistics:**
- Average course rating: {course_data.get('Average Course Rating', 'N/A')}
- Number of reviews: {course_data.get('Number of Reviews', 0)}
- Active participants: {course_data.get('Active Participants', 0)}

**Trainer certification:**
- Type: {course_data.get('Certification', {}).get('Type', 'N/A')}
- Level: {course_data.get('Certification', {}).get('Level', 'N/A')}
- Specialization: {course_data.get('Certification', {}).get('Specialization', 'N/A')}

**Coach's experience:**
- Experience {course_data.get('Experience', {}).get('Years', 'N/A')} years
- Specialization: {course_data.get('Experience', {}).get('Specialization', 'N/A')}
- Courses conducted: {course_data.get('Experience', {}).get('Courses', 'N/A')}
- Coach's rating: {course_data.get('Experience', {}).get('Rating', 'N/A')}

**Course Features:**
- Visual content: {', '.join(course_data.get('Visual Content', [])) or 'N/A'}
- Feedback formats: {', '.join(course_data.get('Trainer Feedback Options', [])) or 'N/A'}
- Tags: {', '.join(course_data.get('Tags', [])) or 'N/A'}

**Program description:**
{course_data.get('Program Description', 'N/A')}

**Training plan:**
{self._format_training_plan(course_data.get('training_plan', []))}
"""
        return formatted.strip()

    def _format_training_plan(self, training_plan: list) -> str:
        """Formats the training plan"""
        if not training_plan:
            return "N/A"
        
        plan_str = ""
        for day in training_plan:
            plan_str += f"\n### {day.get('title', 'Untitled')}\n"
            for exercise in day.get('exercises', []):
                plan_str += (
                    f"- {exercise.get('exercise', 'N/A')}: "
                    f"{exercise.get('sets', 'N/A')} software approach(s)"
                    f"{exercise.get('duration', 'N/A')}, "
                    f"отдых {exercise.get('rest', 'N/A')}\n"
                    f"  ({exercise.get('description', 'without a description')})\n"
                )
        return plan_str

    async def chat(self, request: CourseAssistantRequest) -> CourseAssistantResponse:
        session: tp.List[tp.Dict[str, str]] = self._get_session(request.session_id)

        if not session:
            formatted_course = self._format_course_data(request.course_data)
            prompt_with_course = prompt.format(
                course_data=formatted_course,
            )
            session.append({"role": "system", "content": prompt_with_course})
            session.append(
                {
                    "role": "user",
                    "content": format_initial_user_prompt(
                        request.query, request.user_form
                    ),
                }
            )
        else:
            session.append({"role": "user", "content": request.query})

        response: ChatCompletion = await self.client.chat.completions.create(
            model=self.model,
            messages=session,
        )

        session.append(
            {
                "role": "assistant",
                "content": response.choices[0].message.content,
            }
        )

        self.sessions[request.session_id] = session

        return CourseAssistantResponse(answer=response.choices[0].message.content, session_id=request.session_id)
