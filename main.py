
import streamlit as st

from app.services.resume_service import (
    extract_text_from_pdf
)

from app.services.llm_service import (
    generate_interview_questions
)

from app.services.feedback_service import (
    evaluate_answer
)


st.set_page_config(
    page_title="Mock Interview AI",
    page_icon="🎯",
    layout="wide"
)

st.title("Mock Interview AI")

st.markdown("""
Practice AI-powered mock interviews tailored to your resume and target role.
""")


st.sidebar.title("Mock Interview AI")

st.sidebar.markdown("""
### Features
- Resume Upload
- AI Question Generation
- Answer Evaluation
- Personalized Feedback
""")


role = st.selectbox(
    "Select Interview Role",
    [
        "Software Engineer",
        "Frontend Developer",
        "Backend Developer",
        "Data Analyst",
        "AI/ML Engineer"
    ]
)


uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)


if "questions" not in st.session_state:
    st.session_state.questions = None


if uploaded_file is not None:

    extracted_text = extract_text_from_pdf(
        uploaded_file
    )

    with st.expander(
        "View Extracted Resume Text"
    ):

        st.text_area(
            "Resume Content",
            extracted_text,
            height=250
        )

    if st.button(
        "Generate Interview Questions"
    ):

        with st.spinner(
            "Generating questions..."
        ):

            st.session_state.questions = (
                generate_interview_questions(
                    extracted_text,
                    role
                )
            )

        st.success(
            "Interview questions generated successfully!"
        )

    if st.session_state.questions:

        for index, question in enumerate(
            st.session_state.questions
        ):

            st.divider()

            st.subheader(
                f"Question {index + 1}"
            )

            st.write(question)

            answer = st.text_area(
                f"Your Answer for Question {index + 1}",
                key=f"answer_{index}"
            )

            if st.button(
                f"Evaluate Question {index + 1}",
                key=f"button_{index}"
            ):

                with st.spinner(
                    "Evaluating answer..."
                ):

                    feedback = evaluate_answer(
                        question,
                        answer,
                        role
                    )

                st.markdown(feedback)