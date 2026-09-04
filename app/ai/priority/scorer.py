def score_severity(problem: str, category: str):
    if not problem:
        return 0

    problem_lower = problem.lower()

    score = 10

    severe_terms = [
        "death",
        "fatal",
        "life-threatening",
        "dangerous",
        "unsafe",
        "serious",
        "critical",
        "accident",
        "disaster",
        "emergency",
        "disease",
        "injury",
        "pollution"
    ]

    for term in severe_terms:
        if term in problem_lower:
            score += 3

    category_weights = {
        "disaster_management": 3,
        "health": 2,
        "mining": 3,
        "water_sanitation": 2,
        "environment": 2,
        "tribal_welfare": 1,
        "agriculture": 1,
        "employment": 1,
        "education": 1,
        "infrastructure": 1,
        "urban_development": 1,
        "energy": 2
    }

    score += category_weights.get(category, 0)

    return min(score, 25)


def score_population(affected_group: str, location: str):
    score = 10

    group = affected_group.lower()
    place = location.lower()

    large_groups = [
        "rural communities",
        "urban communities",
        "villagers",
        "students",
        "farmers",
        "workers"
    ]

    vulnerable_groups = [
        "children",
        "women",
        "elderly people",
        "patients",
        "persons with disabilities",
        "people with disabilities",
        "mine workers"
    ]

    if group in large_groups:
        score += 5

    if group in vulnerable_groups:
        score += 5

    broad_locations = [
        "rural areas",
        "urban areas",
        "rural communities",
        "urban communities",
        "rural villages",
        "cities"
    ]

    if place in broad_locations:
        score += 5

    return min(score, 25)


def score_urgency(problem: str, causes: list):
    score = 10

    text = problem.lower()
    causes_text = " ".join(causes).lower()

    urgent_terms = [
        "emergency",
        "immediate",
        "urgent",
        "critical",
        "dangerous",
        "unsafe",
        "life-threatening",
        "accident",
        "disaster",
        "rescue",
        "outbreak",
        "shortage"
    ]

    for term in urgent_terms:
        if term in text or term in causes_text:
            score += 3

    ongoing_terms = [
        "frequent",
        "repeated",
        "ongoing",
        "continuous",
        "regularly",
        "often",
        "currently"
    ]

    for term in ongoing_terms:
        if term in text or term in causes_text:
            score += 2

    seasonal_terms = [
        "monsoon",
        "rainfall",
        "summer",
        "winter",
        "seasonal"
    ]

    for term in seasonal_terms:
        if term in text or term in causes_text:
            score += 2

    return min(score, 25)

def score_impact(problem: str, causes: list, category: str, impact: list):
    score = 10

    text = (
        problem.lower()
        + " "
        + " ".join(causes).lower()
        + " "
        + " ".join(impact).lower()
    )

    impact_terms = [
        "loss",
        "losses",
        "damage",
        "damaging",
        "harm",
        "risk",
        "unsafe",
        "dangerous",
        "pollution",
        "shortage",
        "unemployment",
        "disease",
        "injury"
    ]

    for term in impact_terms:
        if term in text:
            score += 2

    category_weights = {
        "disaster_management": 3,
        "health": 3,
        "mining": 3,
        "water_sanitation": 2,
        "environment": 2,
        "agriculture": 2,
        "employment": 2,
        "education": 1,
        "infrastructure": 1,
        "urban_development": 1,
        "tribal_welfare": 1,
        "energy":2
    }

    score += category_weights.get(category, 0)

    return min(score, 25)


def calculate_priority(
    problem: str,
    category: str,
    affected_group: str,
    location: str,
    causes: list,
    impact: list
):
    severity = score_severity(
        problem,
        category
    )

    population = score_population(
        affected_group,
        location
    )

    urgency = score_urgency(
        problem,
        causes
    )

    impact_score = score_impact(
        problem,
        causes,
        category,
        impact
    )

    base_score = (
        severity
        + population
        + urgency
        + impact_score
    )

    risk_adjustment, risk_reasons = calculate_risk_adjustment(
        problem,
        category,
        affected_group,
        causes
    )

    total_score = min(
        base_score + risk_adjustment,
        100
    )

    if total_score >= 70:
        level = "High"
    elif total_score >= 40:
        level = "Medium"
    else:
        level = "Low"

    return {
        "priority_score": total_score,
        "priority_level": level,
        "factors": {
            "severity": severity,
            "population_affected": population,
            "urgency": urgency,
            "impact": impact_score
        },
        "risk_adjustment": risk_adjustment,
        "risk_reasons": risk_reasons
    }

def calculate_risk_adjustment(
    problem: str,
    category: str,
    affected_group: str,
    causes: list
):
    text = (
        problem.lower()
        + " "
        + " ".join(causes).lower()
    )

    group = affected_group.lower()

    adjustment = 0
    reasons = []

    # High-risk domains
    high_risk_categories = [
        "disaster_management",
        "health",
        "mining"
    ]

    if category in high_risk_categories:
        adjustment += 4
        reasons.append("high-risk domain")

    # Immediate physical safety risk
    safety_terms = [
        "dangerous",
        "unsafe",
        "life-threatening",
        "fatal",
        "death",
        "injury",
        "accident"
    ]

    if any(term in text for term in safety_terms):
        adjustment += 5
        reasons.append("physical safety risk")

    # Vulnerable/high-risk population
    vulnerable_groups = [
        "children",
        "women",
        "elderly people",
        "patients",
        "persons with disabilities",
        "people with disabilities",
        "mine workers"
    ]

    if group in vulnerable_groups:
        adjustment += 3
        reasons.append("vulnerable population")

    # Disaster-related escalation
    disaster_terms = [
        "flood",
        "flooding",
        "drought",
        "lightning",
        "disaster",
        "emergency"
    ]

    if any(term in text for term in disaster_terms):
        adjustment += 4
        reasons.append("disaster risk")

    return adjustment, reasons