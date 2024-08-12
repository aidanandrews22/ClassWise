TOOLS_UPDATE = [
    {
        "type": "function",
        "function": {
            "name": "update_data_collection_booleans",
            "description": "Updates the booleans of the data collection variables. The function accepts a dictionary with boolean values for each data collection field.",
            "parameters": {
                "type": "object",
                "properties": {
                    "updated_booleans": {
                        "type": "object",
                        "description": "A dictionary with keys corresponding to data collection fields and boolean values indicating their status.",
                        "properties": {
                            "interests": {"type": "boolean"},
                            "classes_taken": {"type": "boolean"},
                            "degree": {"type": "boolean"},
                            "major": {"type": "boolean"},
                            "minor": {"type": "boolean"},
                            "gpa": {"type": "boolean"},
                            "year_of_study": {"type": "boolean"},
                            "semesters_left": {"type": "boolean"},
                            "career_goals": {"type": "boolean"},
                            "learning_style": {"type": "boolean"},
                            "time_commitment": {"type": "boolean"},
                            "preferred_subjects": {"type": "boolean"},
                            "academic_strengths": {"type": "boolean"},
                            "academic_weaknesses": {"type": "boolean"},
                            "extracurriculars": {"type": "boolean"},
                        },
                        "additionalProperties": False,
                    },
                },
                "required": ["updated_booleans"],
                "additionalProperties": False,
            },
        },
    }
]

MESSAGES_UPDATE = [
    {
        "role": "system",
        "content": "You are going to help me populate variable for a user.",
    },
    {"role": "user", "content": "Hi, can you tell me the delivery date for my order?"},
]

RESPONSE_FORMAT = {"type": "json_schema", "json_schema": {...}}

INSTRUCTIONS_UPDATE = """
Your goal is to update a dictionary of variables depending on if enough information is gathered to populate each field. A variable is True if enough information is present that a chatbot could use it to reccomend courses for the user. You are to use the function in your tools to fascilitate variable changes. 

Here is the data for each variable:
{self.data}

Here are the current booleans:
{self.data_booleans}
"""
