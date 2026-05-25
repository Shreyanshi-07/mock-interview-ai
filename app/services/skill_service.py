from typing import List


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
    resume_text: str
) -> List[str]:
    """
    Extract detected technical skills from resume text.
    
    Args:
        resume_text: Extracted resume text content
        
    Returns:
        List of detected skills
    """

    detected_skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in resume_text.lower():

            detected_skills.append(skill)

    return detected_skills