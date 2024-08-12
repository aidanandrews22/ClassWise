from openai import OpenAI
from pypdf import PdfReader
from typing import List, Dict, Any
import json
import datetime


client = OpenAI(api_key=api_key)

instructions = """You are an assistant that helps create and update steps in a user's journey based on their resume or input. You will populate each datafield for each node accordingly, leaving some blank if necessary. There is am items List for each step, this list should be populated with anything attached to that step. For example, if there is a project, website, etc assosciated with a step it needs to be included in this variable."""


# add items that can be attached to each object. ie. Projects attached to jobs or education
class Step:
    def __init__(self):
        self.id: int = 1
        self.skills: List[str] = []
        self.keywords: List[str] = []
        self.location: str = ""
        self.industry: List[str] = []
        self.company: str = ""
        self.title: str = ""
        self.items: List[str] = []
        self.time_stamp: str = ""
        self.is_complete: Dict[str, bool] = {
            "skills": False,
            "keywords": False,
            "location": False,
            "industry": False,
            "company": False,
            "title": False,
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "skills": self.skills,
            "keywords": self.keywords,
            "location": self.location,
            "industry": self.industry,
            "company": self.company,
            "title": self.title,
            "is_complete": self.is_complete,
            "items": self.items,
            "time_stamp": self.time_stamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Step":
        step = cls()
        step.id = 1
        step.skills = data.get("skills", [])
        step.keywords = data.get("keywords", [])
        step.location = data.get("location", "")
        step.industry = data.get("industry", [])
        step.company = data.get("company", "")
        step.title = data.get("title", "")
        step.time_stamp = data.get("time_stamp", [])
        step.is_complete = data.get("is_complete", {})
        step.items = data.get("items", [])
        return step


assistant = client.beta.assistants.create(
    instructions="You are an assistant that helps create and update steps in a user's journey based on their resume or input.",
    model="gpt-4o-mini",
    tools=[
        {
            "type": "function",
            "function": {
                "name": "create_step",
                "description": "Create a new step in the user's journey",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "skills": {"type": "array", "items": {"type": "string"}},
                        "keywords": {"type": "array", "items": {"type": "string"}},
                        "location": {"type": "string"},
                        "industry": {"type": "array", "items": {"type": "string"}},
                        "company": {"type": "string"},
                        "title": {"type": "string"},
                        "items": {"type": "array", "items": {"type": "string"}},
                        "time_stamp": {"type": "string"},
                    },
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "update_step",
                "description": "Update an existing step in the user's journey",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "skills": {"type": "array", "items": {"type": "string"}},
                        "keywords": {"type": "array", "items": {"type": "string"}},
                        "location": {"type": "string"},
                        "industry": {"type": "array", "items": {"type": "string"}},
                        "company": {"type": "string"},
                        "title": {"type": "string"},
                        "items": {"type": "array", "items": {"type": "string"}},
                        "time_stamp": {"type": "string"},
                    },
                    "required": ["id"],
                },
            },
        },
    ],
)


def create_step(
    skills=None,
    keywords=None,
    location=None,
    industry=None,
    company=None,
    title=None,
    items=None,
    time_stamp=None,
):
    step = Step()
    if skills:
        step.skills = skills
    if keywords:
        step.keywords = keywords
    if location:
        step.location = location
    if industry:
        step.industry = industry
    if company:
        step.company = company
    if title:
        step.title = title
    if items:
        step.items = items
    step.id = 1  # Identification for the step in the db probably related to user_id
    return json.dumps(step.to_dict())


def update_step(
    id,
    skills=None,
    keywords=None,
    location=None,
    industry=None,
    company=None,
    title=None,
    items=None,
    time_stamp=None,
):
    step = Step()  # Need to populate with existing steps
    step.id = id
    if skills:
        step.skills = skills
    if keywords:
        step.keywords = keywords
    if location:
        step.location = location
    if industry:
        step.industry = industry
    if company:
        step.company = company
    if title:
        step.title = title
    if items:
        step.items = items
    return json.dumps(step.to_dict())


reader = PdfReader("../data/resume/Aidan_Andrews_Resume.pdf")
full_text = ""
for page in reader.pages:
    full_text += page.extract_text()
print(full_text)
thread = client.beta.threads.create()
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=full_text,
)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="""Extract relevant information from the resume and create steps in the user's journey. Store this as a json. Here is an example of the nodes you are building: 
{
  "step": {
    "id": 1,
    "skills": [
      "Skill 1",
      "Skill 2",
      "Skill 3"
    ],
    "keywords": [
      "Keyword 1",
      "Keyword 2",
      "Keyword 3"
    ],
    "location": "City, State/Country",
    "industry": [
      "Industry 1",
      "Industry 2"
    ],
    "company": "Company Name",
    "title": "Job Title",
    "items": [
      "Project 1",
      "Achievement 1",
      "Responsibility 1"
    ],
    "time_stamp": "2021-2024",
  }
}""",
)


def handle_tool_calls(tool_calls):
    tool_outputs = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)

        if function_name == "create_step":
            output = create_step(**function_args)
        elif function_name == "update_step":
            output = update_step(**function_args)
        else:
            output = json.dumps({"error": "Unknown function"})

        tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

    return tool_outputs


while run.status != "completed":
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    if run.status == "requires_action":
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = handle_tool_calls(tool_calls)
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id, run_id=run.id, tool_outputs=tool_outputs
        )

messages = client.beta.threads.messages.list(thread_id=thread.id)
for message in messages.data:
    if message.role == "assistant":
        print(message.content[0].text.value)
