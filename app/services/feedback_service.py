from app.services.llm_service import client


def evaluate_answer(
    question,
    answer,
    role
):

    prompt = f"""
    You are an expert technical interviewer.

    Evaluate the candidate's answer.

    Role:
    {role}

    Interview Question:
    {question}

    Candidate Answer:
    {answer}

    Give:

    1. Score out of 10
    2. Strengths
    3. Weaknesses
    4. Improvement suggestions

    Keep feedback concise and professional.
    """

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"Error generating feedback: {str(e)}"