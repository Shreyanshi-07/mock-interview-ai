import matplotlib.pyplot as plt
import numpy as np

def create_radar_chart(
    feedback
):

    labels = [
        "Technical",
        "Communication",
        "Problem Solving",
        "Confidence"
    ]

    scores = [
        feedback["technical_score"],
        feedback["communication_score"],
        feedback["problem_solving"],
        feedback["confidence"]
    ]

    scores += scores[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw=dict(
            polar=True
        )
    )

    ax.plot(
        angles,
        scores
    )

    ax.fill(
        angles,
        scores,
        alpha=0.25
    )

    ax.set_xticks(
        angles[:-1]
    )

    ax.set_xticklabels(
        labels
    )

    ax.set_ylim(
        0,
        10
    )

    return fig
def save_radar_chart(
    feedback,
    filename="radar_chart.png"
):

    fig = create_radar_chart(
        feedback
    )

    fig.savefig(
        filename,
        bbox_inches="tight"
    )

    return filename