import os
import json
from google import genai

from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_interview_questions(
    resume_text,
    role
):

    prompt = f"""
You are a technical interviewer.

Generate exactly 5 interview questions.

Return ONLY valid JSON.

Example:
[
  "Question 1",
  "Question 2"
]

Role:
{role}

Resume:
{resume_text[:3000]}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )


        questions = json.loads(
            response.text
        )

        return questions

    except Exception:

       

        return [
        "Tell me about yourself.",
        "Explain a challenging project you worked on.",
        "What are your strengths and weaknesses?",
        "Describe a difficult bug you fixed.",
        "Why do you want this role?"
    ]