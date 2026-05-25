import streamlit as st
import time
from app.constants import INTERVIEW_ROLES, DIFFICULTY_LEVELS, TIMER_OPTIONS

from app.services.report_service import (
    generate_report
)
from app.services.resume_service import (
    extract_text_from_pdf
)

from app.services.llm_service import (
    generate_interview_questions
)
from app.services.chart_service import (
    create_radar_chart
)
from app.services.feedback_service import (
    evaluate_answer
)
from app.services.skill_service import (
    extract_skills
)

st.set_page_config(
    page_title="Mock Interview AI",
    page_icon="🎯",
    layout="wide"
)

st.markdown(
    """
    <h1 style='
        font-size:48px;
        font-weight:700;
        color:#F8F9F9;
        margin-bottom:0;
    '>
        Mock Interview AI
    </h1>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <p style='
        font-size:18px;
        color:#D5D8DC;
        margin-top:0;
        margin-bottom:10px;
    '>
        AI-powered interview preparation platform
        with intelligent evaluation analytics.
    </p>
    """,
    unsafe_allow_html=True
)
st.markdown("""
<style>
hr {
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)
st.divider()


st.sidebar.title("Mock Interview AI")

st.sidebar.markdown(
    """
    ## Platform Features

    ✅ Resume Analysis

    ✅ AI Question Generation

    ✅ Adaptive Difficulty Levels

    ✅ AI-Powered Evaluation

    ✅ Analytics Dashboard

    ✅ Executive PDF Reports
    """
)


role = st.selectbox("Select Interview Role", INTERVIEW_ROLES)

difficulty = st.selectbox(
    "Select Difficulty Level",
    DIFFICULTY_LEVELS
)

timer_minutes = st.selectbox(
    "Interview Timer (Minutes)",
    TIMER_OPTIONS
)


uploaded_file = st.file_uploader(
    "Upload your resume (PDF only)",
    type=["pdf"]
)


if "questions" not in st.session_state:
    st.session_state.questions = None

if "start_time" not in st.session_state:

    st.session_state.start_time = None

if uploaded_file is not None:
    try:
        extracted_text = extract_text_from_pdf(uploaded_file)
        
        if not extracted_text or len(extracted_text.strip()) < 50:
            st.error("⚠️ Could not extract meaningful text from the PDF. Please make sure it's a valid resume.")
            st.stop()
            
    except Exception as e:
        st.error(f"⚠️ Error reading PDF: {str(e)}")
        st.stop()
    skills = extract_skills(
        extracted_text
)
    with st.expander(
        "View Extracted Resume Text"
    ):

        st.code(
            extracted_text[:1500]
)
    if skills:

        st.subheader(
        "Detected Skills"
    )

        st.success(
        ", ".join(skills)
    )

    if st.button("Generate Interview Questions"):
        try:
            with st.spinner("🤖 Analyzing your resume and generating questions..."):
                st.session_state.questions = generate_interview_questions(
                    extracted_text,
                    role,
                    skills,
                    difficulty
                )
                st.session_state.start_time = time.time()
                st.success("Questions generated successfully!")
        except Exception as e:
            st.error(f"⚠️ Failed to generate questions: {str(e)}")
            st.error("Please check your API key in the .env file")
            

            st.session_state.start_time = (
            time.time()
    )

    if st.session_state.questions:

        for index, question in enumerate(
            st.session_state.questions
        ):
            if st.session_state.start_time:
                elapsed_time = (
                time.time()
            -   st.session_state.start_time
)

            remaining_time = max(
            0,
            timer_minutes * 60 - int(elapsed_time)
)

            minutes = remaining_time // 60

            seconds = remaining_time % 60

            st.warning(
            f"⏳ Time Remaining: {minutes:02}:{seconds:02}"
)
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

                    st.markdown(
                            f"""
                        <div style="
                            background-color:#1F618D;
                            padding:20px;
                            border-radius:15px;
                            text-align:center;
                            color:white;
                            margin-bottom:15px;
                        ">
                            <h3>Technical Knowledge</h3>
                            <h1>
                                {st.session_state[feedback_key]['technical_score']}/10
                            </h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#117864;
                            padding:20px;
                            border-radius:15px;
                            text-align:center;
                            color:white;
                        ">
                            <h3>Problem Solving</h3>
                            <h1>
                                {st.session_state[feedback_key]['problem_solving']}/10
                            </h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with col2:

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#7D3C98;
                            padding:20px;
                            border-radius:15px;
                            text-align:center;
                            color:white;
                            margin-bottom:15px;
                        ">
                            <h3>Communication</h3>
                            <h1>
                                {st.session_state[feedback_key]['communication_score']}/10
                            </h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div style="
                            background-color:#CA6F1E;
                            padding:20px;
                            border-radius:15px;
                            text-align:center;
                            color:white;
                        ">
                            <h3>Confidence</h3>
                            <h1>
                                {st.session_state[feedback_key]['confidence']}/10
                            </h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    chart = create_radar_chart(
                            st.session_state[
                                feedback_key
                        ]
                    )

                    st.pyplot(chart)
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

                st.divider()

    latest_feedback = None

    for index, question in enumerate(
        st.session_state.questions or []
        ):

        feedback_key = (
            f"feedback_{index}"
        )

        if feedback_key in st.session_state:

            latest_feedback = (
                st.session_state[
                    feedback_key
                ]
            )

    if latest_feedback:

        st.subheader(
            "Final Interview Report"
        )

        report_file = generate_report(
            latest_feedback,
            role
        )

        with open(
            report_file,
            "rb"
        ) as pdf_file:

            st.download_button(
                label="Download Full Interview Report",
                data=pdf_file,
                file_name="interview_report.pdf",
                mime="application/pdf"
            )

        st.divider()