import os

from google import genai

from dotenv import load_dotenv


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_interview_questions(resume_text,role):

    prompt = f"""
    You are a technical interviewer.

    Based on the following resume,
    generate:

    1. 5 technical interview questions
    2. 3 behavioral interview questions
    3. 2 project-related questions
    Target Role:
    {role}
    Resume:
    {resume_text[:3000]}
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error generating questions: {str(e)}"