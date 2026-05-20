from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter


def generate_report(
    feedback,
    filename="interview_report.pdf"
):

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    elements = []

    title = Paragraph(
        "Mock Interview Report",
        styles["Title"]
    )

    elements.append(title)

    elements.append(
        Spacer(1, 12)
    )

    metrics = [
        f"Technical Knowledge: {feedback['technical_score']}/10",
        f"Communication: {feedback['communication_score']}/10",
        f"Problem Solving: {feedback['problem_solving']}/10",
        f"Confidence: {feedback['confidence']}/10"
    ]

    for metric in metrics:

        elements.append(
            Paragraph(
                metric,
                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Strengths",
            styles["Heading2"]
        )
    )

    for strength in feedback["strengths"]:

        elements.append(
            Paragraph(
                f"• {strength}",
                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Weaknesses",
            styles["Heading2"]
        )
    )

    for weakness in feedback["weaknesses"]:

        elements.append(
            Paragraph(
                f"• {weakness}",
                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 12)
    )

    elements.append(
        Paragraph(
            "Improvement Suggestions",
            styles["Heading2"]
        )
    )

    for improvement in feedback[
        "improvements"
    ]:

        elements.append(
            Paragraph(
                f"• {improvement}",
                styles["BodyText"]
            )
        )

    doc.build(elements)

    return filename