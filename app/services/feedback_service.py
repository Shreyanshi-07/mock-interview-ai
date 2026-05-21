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


TECH_KEYWORDS = [
    "algorithm",
    "database",
    "api",
    "function",
    "class",
    "object",
    "optimization",
    "frontend",
    "backend",
    "sql",
    "python",
    "react",
    "git",
    "debugging",
    "performance"
]


def evaluate_with_gemini(
    question,
    answer,
    role
):

    prompt = f"""
You are an expert technical interviewer.

Evaluate this interview answer.

Question:
{question}

Answer:
{answer}

Role:
{role}

Return ONLY valid JSON.

Example:
{{
    "technical_score": 8,
    "communication_score": 7,
    "problem_solving": 8,
    "confidence": 7,

    "summary": "The candidate demonstrated strong technical understanding and clear communication, but could improve depth in scalability discussions.",

    "strengths": [
        "Good technical explanation"
    ],

    "weaknesses": [
        "Could provide more examples"
    ],

    "improvements": [
        "Discuss scalability considerations"
    ]
}}
"""

    print("Gemini evaluation running...")

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


def evaluate_answer(

    question,
    answer,
    role
):

    try:

        return evaluate_with_gemini(
            question,
            answer,
            role
        )

    except Exception as e:

        print(e)

    answer_lower = answer.lower()

    keyword_matches = 0

    for keyword in TECH_KEYWORDS:

        if keyword in answer_lower:

            keyword_matches += 1

    answer_length = len(
        answer.split()
    )

    technical_score = min(
        10,
        4 + keyword_matches
    )

    communication_score = min(
        10,
        answer_length // 15 + 3
    )

    problem_solving = min(
        10,
        keyword_matches + 4
    )

    confidence = min(
        10,
        answer_length // 20 + 4
    )

    strengths = []

    weaknesses = []

    improvements = []

    if keyword_matches >= 3:

        strengths.append(
            "Good use of technical terminology."
        )

    else:

        weaknesses.append(
            "Answer lacks technical depth."
        )

        improvements.append(
            "Include more technical concepts and examples."
        )

    if answer_length >= 60:

        strengths.append(
            "Detailed explanation provided."
        )

    else:

        weaknesses.append(
            "Answer could be more detailed."
        )

        improvements.append(
            "Expand explanations with examples and reasoning."
        )

    if not strengths:

        strengths.append(
            "Attempted to answer the question."
        )

    return {

    "technical_score": technical_score,

    "communication_score": communication_score,

    "problem_solving": problem_solving,

    "confidence": confidence,

    "summary":
    "Candidate showed moderate interview performance with room for improvement in technical depth and communication clarity.",

    "strengths": strengths,

    "weaknesses": weaknesses,

    "improvements": improvements
}