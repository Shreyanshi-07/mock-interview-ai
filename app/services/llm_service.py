import os
import json

from google import genai

from dotenv import load_dotenv
load_dotenv()

client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)
USE_MOCK_DATA = True


SKILL_QUESTIONS = {

    "Python": [
        "What is list comprehension in Python?",
        "Explain the difference between lists and tuples.",
    ],

    "SQL": [
        "Explain different types of SQL joins.",
        "What is normalization in databases?",
    ],

    "React": [
        "What are React hooks?",
        "Explain virtual DOM in React.",
    ],

    "Java": [
        "Explain OOP concepts in Java.",
        "What is the difference between JDK and JRE?",
    ],

    "Machine Learning": [
        "What is overfitting in machine learning?",
        "Explain supervised vs unsupervised learning.",
    ],

    "Streamlit": [
        "How does session state work in Streamlit?",
        "What are Streamlit widgets?",
    ],

    "Git": [
        "What is the difference between git merge and git rebase?",
        "Explain the purpose of git branching.",
    ]
}

def generate_with_gemini(

    role,
    skills,
    difficulty
):

    prompt = f"""
You are an expert technical interviewer.

Generate 5 interview questions.

Role:
{role}

Skills:
{skills}

Difficulty:
{difficulty}

Return ONLY valid JSON list.

Example:
[
    "What is API authentication?",
    "Explain SQL joins."
]
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    cleaned_response = (
        response.text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    return json.loads(
        cleaned_response
    )
    
def generate_interview_questions(
    resume_text,
    role,
    skills,
    difficulty
):

        if not USE_MOCK_DATA:

            try:

                return generate_with_gemini(
                    role,
                    skills,
                    difficulty
                )

            except Exception as e:

                print(e)

        difficulty_multiplier = {

            "Beginner": 1,
            "Intermediate": 2,
            "Advanced": 3
        }

        questions = []

        for skill in skills:

            if skill in SKILL_QUESTIONS:

                selected_questions = (
                    SKILL_QUESTIONS[skill]
                )

                questions.extend(
                    selected_questions[
                        :difficulty_multiplier[
                            difficulty
                        ]
                    ]
                )

        if len(questions) < 5:

            questions.extend([
                "Tell me about yourself.",
                "Explain a challenging project you worked on.",
                "Why do you want this role?"
            ])

        return questions[:5]