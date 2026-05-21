COMMON_SKILLS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "React",
    "Node.js",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "Data Analysis",
    "Streamlit",
    "Git",
    "HTML",
    "CSS",
    "Flask",
    "Django",
    "TensorFlow",
    "Pandas",
    "NumPy"
]


def extract_skills(
    resume_text
):

    detected_skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in resume_text.lower():

            detected_skills.append(skill)

    return detected_skills