USE_MOCK_DATA = True


def evaluate_answer(
    question,
    answer,
    role
):

    if USE_MOCK_DATA:

        return {
            "technical_score": 8,
            "communication_score": 7,
            "problem_solving": 9,
            "confidence": 6,
            "strengths": [
                "Good technical understanding",
                "Clear explanation"
            ],
            "weaknesses": [
                "Could improve answer structure"
            ],
            "improvements": [
                "Practice concise communication",
                "Use more real-world examples"
            ]
        }

    # REAL GEMINI LOGIC LATER