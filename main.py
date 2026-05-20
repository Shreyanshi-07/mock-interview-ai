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
    page_title="Mock Interview AI"
)

st.title("Mock Interview AI")


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

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume Content",
        extracted_text,
        height=250
    )

    if st.button("Generate Interview Questions"):

        with st.spinner("Generating questions..."):

            st.session_state.questions = (
                generate_interview_questions(
                    extracted_text,
                    role
                )
            )

    if st.session_state.questions:

        st.subheader("AI Interview Questions")

        st.markdown(
            st.session_state.questions
        )

        user_answer = st.text_area(
            "Write your answer here",
            height=200
        )

        if st.button("Evaluate My Answer"):

            with st.spinner(
                "Evaluating answer..."
            ):

                feedback = evaluate_answer(
                    st.session_state.questions,
                    user_answer,
                    role
                )

            st.subheader("AI Feedback")

            st.markdown(feedback)