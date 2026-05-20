USE_MOCK_DATA = True


def generate_interview_questions(
    resume_text,
    role
):

    if USE_MOCK_DATA:

        return [
            "Tell me about yourself.",
            "Explain a challenging project you worked on.",
            "How would you debug a slow application?",
            "Describe a difficult bug you fixed.",
            "Why are you interested in this role?"
        ]