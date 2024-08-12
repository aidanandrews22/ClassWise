import os
import json
import pypdf
from typing import Dict, List, Any
from openai import OpenAI
from dotenv_vault import load_dotenv

from assets import RESPONSE_FORMAT, TOOLS_UPDATE, MESSAGES_UPDATE, INSTRUCTIONS_UPDATE

load_dotenv()


class UserNode:
    def __init__(self, user_id: str, pdf_paths: List = [], chat_history: str = ""):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.openai_api_key)

        self.messages_update = MESSAGES_UPDATE
        self.tools_update = TOOLS_UPDATE
        self.instructions_update = INSTRUCTIONS_UPDATE

        self.user_id = user_id
        self.pdf_paths = pdf_paths
        self.chat_history = chat_history

        self.pdfs: Dict[str, str] = {}  # Dictionary[pdf_path, pdf_raw_text]

        self.user_id = user_id
        self.data = {
            "interests": [],
            "classes_taken": [],
            "degree": "",
            "major": "",
            "minor": "",
            "gpa": 0.0,
            "year_of_study": 0,
            "semesters_left": 0,
            "career_goals": [],
            "learning_style": "",
            "time_commitment": "",
            "preferred_subjects": [],
            "academic_strengths": [],
            "academic_weaknesses": [],
            "extracurriculars": [],
        }
        self.data_booleans = {
            "interests": False,
            "classes_taken": False,
            "degree": False,
            "major": False,
            "minor": False,
            "gpa": False,
            "year_of_study": False,
            "semesters_left": False,
            "career_goals": False,
            "learning_style": False,
            "time_commitment": False,
            "preferred_subjects": False,
            "academic_strengths": False,
            "academic_weaknesses": False,
            "extracurriculars": False,
        }

        self.data_completion = {field: False for field in self.data.keys()}
        self.recommendation_ready = False

        # population
        self.populate_pdfs()
        print(self.pdfs)
        self.populate_user_info()

    def populate_pdfs(self):
        for pdf_path in self.pdf_paths:
            reader = pypdf.PdfReader(pdf_path)
            full_text = ""
            for page in reader.pages:
                full_text += page.extract_text()
            self.pdfs[pdf_path] = full_text

    def populate_user_info(self, error: str = ""):
        # assistant = self.client.beta.assistants.create(
        #     instructions=self.instructions,
        #     model="gpt-3.5-turbo",
        #     messages=self.messages,
        #     tools=self.tools,
        #     temperature=0.2,  # makes the model more deterministic (0-2 where 2 is most random)
        #     response_format=RESPONSE_FORMAT,
        # )
        return

    def update_data_collection_booleans(self, updated_booleans: Dict[str, bool]):
        for key, value in updated_booleans.items():
            if key in self.data_booleans:
                self.data_booleans[key] = value
            else:
                self.populate_user_info(
                    error=f"Unexpected key: {key}. Please check the inputs."
                )

    def update_variables(self):
        assistant = self.client.beta.assistants.create(
            instructions=self.instructions_update,
            model="gpt-3.5-turbo",
            messages=self.messages_update,
            tools=self.tools_update,
            temperature=0,  # makes the model more deterministic (0-2 where 2 is most random)
        )

    def is_recommendation_ready(self) -> bool:
        self.update_variables()
        for key, value in self.data_booleans:
            if not value:
                return False
        return True
