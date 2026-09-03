import re
def extract_problem(challenge: str):
    """
    Extract a structured representation of a societal challenge.
    """

    if not challenge or not challenge.strip():
        return {
            "problem": "",
            "affected_group": "",
            "location": "",
            "causes": [],
            "impact": []
        }

    text = re.sub(r"\s+", " ", challenge.strip())

    return {
        "problem": extract_problem_statement(text),
        "affected_group": extract_affected_group(text),
        "location": extract_location(text),
        "causes": extract_causes(text),
        "impact": extract_impact(text)
    }


def extract_problem_statement(text: str):
    """
    Extract the core problem from common problem-description patterns.
    """

    patterns = [
        r"(?:do not have access to|lack access to)\s+(.+?)(?:\s+because|\s+due to|$)",

        r"(?:lack of|shortage of|limited access to|limited availability of)\s+(.+?)(?:\s+because|\s+due to|$)",

        r"(?:are struggling with|struggling with|are facing|face|facing)\s+(.+?)(?:\s+because|\s+due to|$)",

        r"(?:are exposed to|exposed to|suffer from|suffering from)\s+(.+?)(?:\s+because|\s+due to|$)",

        r"(?:have to travel|must travel|need to travel)\s+(.+?)(?:\s+because|\s+due to|$)"
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            problem = match.group(1).strip()
            return problem.rstrip("., ")

    return text


def extract_affected_group(text: str):
    """
    Extract the main population affected by the challenge.
    """

    groups = [
        "persons with disabilities",
        "people with disabilities",
        "mine workers",
        "rural communities",
        "urban communities",
        "students",
        "farmers",
        "patients",
        "children",
        "women",
        "elderly people",
        "workers",
        "teachers",
        "villagers"
    ]

    text_lower = text.lower()

    for group in groups:
        if group in text_lower:
            return group

    return ""


def extract_location(text: str):
    """
    Extract geographic location/context.

    Facilities such as hospitals, schools and mines are
    deliberately not treated as geographic locations.
    """

    locations = [
        "rural areas",
        "urban areas",
        "rural communities",
        "urban communities",
        "rural villages",
        "villages",
        "cities",
        "rural regions",
        "urban regions"
    ]

    text_lower = text.lower()

    for location in locations:
        if location in text_lower:
            return location

    return ""


def extract_causes(text: str):
    """
    Extract causes introduced by causal expressions.
    """

    causes = []

    patterns = [
        r"\bbecause\s+(.+?)(?:\.|$)",
        r"\bdue to\s+(.+?)(?:\.|$)",
        r"\bbecause of\s+(.+?)(?:\.|$)"
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            cause_text = match.strip()

            parts = re.split(
                r"\s+and\s+|\s*,\s*",
                cause_text,
                flags=re.IGNORECASE
            )

            for part in parts:

                part = part.strip()

                if part:
                    causes.append(
                        clean_cause(part)
                    )

    return remove_duplicates(causes)


def clean_cause(cause: str):
    """
    Normalize a cause phrase.
    """

    cause = cause.strip(" .,")

    # Convert statements such as:
    # "schools lack computers"
    # into:
    # "lack of computers"
    cause = re.sub(
        r"^schools?\s+lack\s+",
        "lack of ",
        cause,
        flags=re.IGNORECASE
    )

    # Convert:
    # "hospitals lack adequate medical facilities"
    # into:
    # "lack of adequate medical facilities"
    cause = re.sub(
        r"^(?:nearby\s+)?hospitals?\s+lack\s+",
        "lack of ",
        cause,
        flags=re.IGNORECASE
    )

    return cause


def extract_impact(text: str):
    """
    Extract explicitly stated consequences and impacts.
    """

    impacts = []

    patterns = [
        r"\bleads to\s+(.+?)(?:\.|$)",
        r"\bresults in\s+(.+?)(?:\.|$)",
        r"\bcausing\s+(.+?)(?:\.|$)",
        r"\baffecting\s+(.+?)(?:\.|$)",
        r"\bresulting in\s+(.+?)(?:\.|$)"
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:

            impact = match.strip(" .,")

            if impact:
                impacts.append(impact)

    access_match = re.search(
        r"(?:do not have access to|lack access to)\s+(.+?)(?:\s+because|\s+due to|$)",
        text,
        flags=re.IGNORECASE
    )

    if access_match:

        impacts.append(
            "limited access to "
            + access_match.group(1).strip(" .,")
        )

    return remove_duplicates(impacts)


def remove_duplicates(items):
    """
    Remove duplicate values while preserving order.
    """

    seen = set()
    result = []

    for item in items:

        normalized = item.lower()

        if normalized not in seen:

            seen.add(normalized)
            result.append(item)

    return result