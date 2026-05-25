from typing import Dict, Any

from reportlab.platypus import (
    KeepTogether
)

from reportlab.platypus import (
    Image
)

from app.services.chart_service import (
    save_radar_chart
)

from reportlab.lib.enums import (
    TA_CENTER
)

from reportlab.lib.styles import (
    ParagraphStyle
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.platypus import HRFlowable

from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import letter

from datetime import datetime


def generate_report(
    feedback: Dict[str, Any],
    role: str,
    filename: str = "interview_report.pdf"
) -> str:
    """
    Generate a professional PDF interview report.
    
    Args:
        feedback: Dictionary containing interview evaluation data
        role: Target interview role
        filename: Output PDF filename
        
    Returns:
        Path to the generated PDF report
    """

    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#1B2631")
    )

    section_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#154360"),
        spaceAfter=12
    )

    summary_style = ParagraphStyle(
        "Summary",
        parent=styles["BodyText"],
        fontSize=11,
        leading=18
    )

    elements = []

    current_date = datetime.now().strftime(
        "%B %d, %Y"
    )

    title = Paragraph(
        "AI Mock Interview Report",
        title_style
    )

    elements.append(title)

    elements.append(
        Spacer(1, 20)
    )

    metadata = [
        f"<b>Role Applied For:</b> {role}",
        f"<b>Generated On:</b> {current_date}"
    ]

    for item in metadata:

        elements.append(
            Paragraph(
                item,
                styles["BodyText"]
            )
        )

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        HRFlowable(
            width="100%"
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    overall_score = round(
        (
            feedback["technical_score"]
            + feedback["communication_score"]
            + feedback["problem_solving"]
            + feedback["confidence"]
        ) / 4,
        1
    )

    if overall_score >= 8:

        status = "STRONG HIRE"

        status_color = "#1E8449"

    elif overall_score >= 6:

        status = "HIRE"

        status_color = "#2E86C1"

    elif overall_score >= 4:

        status = "HOLD"

        status_color = "#CA6F1E"

    else:

        status = "NO HIRE"

        status_color = "#C0392B"

    score_box = Table(
        [[
            Paragraph(
                f"""
                <para align=center>
                <font size=24 color='white'>
                <b>{overall_score}/10</b>
                </font>
                <br/>
                <font size=12 color='white'>
                Overall Interview Score
                </font>
                </para>
                """,
                styles["BodyText"]
            )
        ]],
        colWidths=[400]
    )

    chart_path = save_radar_chart(
        feedback
    )

    score_box.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor("#1F618D")
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                0,
                colors.white
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                20
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                20
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            )
        ])
    )

    elements.append(score_box)

    status_box = Table(
        [[
            Paragraph(
                f"""
                <para align=center>
                <font size=12 color='white'>
                <b>{status}</b>
                </font>
                </para>
                """,
                styles["BodyText"]
            )
        ]],
        colWidths=[160]
    )

    status_box.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, -1),
                colors.HexColor(
                    status_color
                )
            ),

            (
                "ALIGN",
                (0, 0),
                (-1, -1),
                "CENTER"
            ),

            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                8
            ),

            (
                "BOX",
                (0, 0),
                (-1, -1),
                0,
                colors.white
            )
        ])
    )

    status_box.hAlign = "CENTER"

    elements.append(status_box)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Spacer(1, 25)
    )

    summary = Paragraph(
        feedback["summary"],
        summary_style
    )

    elements.append(summary)

    elements.append(
        Spacer(1, 20)
    )

    table_data = [
        ["Competency", "Score"],
        [
            "Technical Knowledge",
            f"{feedback['technical_score']}/10"
        ],
        [
            "Communication",
            f"{feedback['communication_score']}/10"
        ],
        [
            "Problem Solving",
            f"{feedback['problem_solving']}/10"
        ],
        [
            "Confidence",
            f"{feedback['confidence']}/10"
        ]
    ]

    table = Table(
        table_data,
        colWidths=[250, 100]
    )

    table.hAlign = "CENTER"

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#154360")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 1, colors.grey),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),

            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),

            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
                colors.whitesmoke,
                colors.lightgrey
            ]),
        ])
    )

    elements.append(table)

    elements.append(
        Spacer(1, 25)
    )

    chart = Image(
        chart_path,
        width=300,
        height=300
    )

    chart.hAlign = "CENTER"

    elements.append(chart)

    elements.append(
        Spacer(1, 20)
    )

    elements.append(
        Paragraph(
            "Strengths",
            section_style
        )
    )

    for strength in feedback["strengths"]:

        elements.append(
            Paragraph(
                f"• {strength}",
                summary_style
            )
        )

    elements.append(
        Spacer(1, 16)
    )

    elements.append(
        Paragraph(
            "Weaknesses",
            section_style
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
        Spacer(1, 16)
    )

    elements.append(
        Paragraph(
            "Improvement Suggestions",
            section_style
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

    elements.append(
        Spacer(1, 15)
    )

    footer = Paragraph(
        "Generated by Mock Interview AI",
        styles["Italic"]
    )

    elements.append(footer)

    doc.build(elements)

    return filename