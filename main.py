import streamlit as st
from app.services.report_service import (
    generate_report
)
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

        st.session_state.questions = (
            generate_interview_questions(
                extracted_text,
                role
            )
        )

    if st.session_state.questions:

        for index, question in enumerate(
            st.session_state.questions
        ):

            feedback_key = (
                f"feedback_{index}"
            )

            st.markdown(
                f"### Question {index + 1}"
            )

            st.info(question)

            answer = st.text_area(
                f"Your Answer for Question {index + 1}",
                key=f"answer_{index}"
            )

            if st.button(
                f"Evaluate Question {index + 1}",
                key=f"button_{index}"
            ):

                st.session_state[
                    feedback_key
                ] = evaluate_answer(
                    question,
                    answer,
                    role
                )

            if feedback_key in st.session_state:

                st.subheader(
                    "AI Feedback Dashboard"
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Technical Knowledge",
                        f"{st.session_state[feedback_key]['technical_score']}/10"
                    )

                    st.metric(
                        "Problem Solving",
                        f"{st.session_state[feedback_key]['problem_solving']}/10"
                    )

                with col2:

                    st.metric(
                        "Communication",
                        f"{st.session_state[feedback_key]['communication_score']}/10"
                    )

                    st.metric(
                        "Confidence",
                        f"{st.session_state[feedback_key]['confidence']}/10"
                    )

                st.subheader("Strengths")

                for strength in st.session_state[
                    feedback_key
                ]["strengths"]:

                    st.success(strength)

                st.subheader("Weaknesses")

                for weakness in st.session_state[
                    feedback_key
                ]["weaknesses"]:

                    st.error(weakness)

                st.subheader(
                    "Improvement Suggestions"
                )

                for improvement in st.session_state[
                    feedback_key
                ]["improvements"]:

                    st.info(improvement)

                report_file = generate_report(
                    st.session_state[feedback_key]
                )

                with open(
                    report_file,
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        label="Download Interview Report",
                        data=pdf_file,
                        file_name="interview_report.pdf",
                        mime="application/pdf",
                        key=f"download_{index}"
                    )

            st.divider()