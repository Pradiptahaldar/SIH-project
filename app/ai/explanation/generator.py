def generate_explanation(
    challenge: str,
    category: dict,
    extraction: dict,
    priority: dict
):
    """
    Generate a human-readable explanation for the AI analysis.
    """

    category_label = category["category_label"]
    confidence = category["confidence"]

    problem = extraction["problem"]
    affected_group = extraction["affected_group"]
    location = extraction["location"]
    causes = extraction["causes"]

    priority_score = priority["priority_score"]
    priority_level = priority["priority_level"]

    explanation = []

    # Category explanation
    explanation.append(
        f"The challenge was classified as '{category_label}' "
        f"with a confidence of {confidence:.3f}."
    )

    # Problem explanation
    if problem:
        explanation.append(
            f"The identified problem is '{problem}'."
        )

    # Affected group
    if affected_group:
        explanation.append(
            f"The affected group is '{affected_group}'."
        )

    # Location
    if location:
        explanation.append(
            f"The affected location or context is '{location}'."
        )

    # Causes
    if causes:
        cause_text = ", ".join(causes)
        explanation.append(
            f"The identified causes include {cause_text}."
        )

    # Priority explanation
    explanation.append(
        f"The challenge received a priority score of {priority_score}/100, "
        f"placing it in the '{priority_level}' priority level."
    )

    return {
        "summary": " ".join(explanation),
        "category_reason": (
            f"The challenge matches the '{category_label}' domain "
            f"based on its semantic meaning."
        ),
        "priority_reason": (
            f"The priority level is '{priority_level}' with a score "
            f"of {priority_score}/100."
        )
    }