from app.ai.semantic.classifier import classify_semantic
def fuse_category(challenge: str):
    """
    Combine semantic understanding with contextual evidence
    to produce a final category decision.
    """

    semantic_result = classify_semantic(challenge)

    category = semantic_result["category"]
    semantic_score = semantic_result["semantic_score"]

    # Initial contextual signals.
    text = challenge.lower()

    context_scores = {
        "disaster_management": 0.0,
        "agriculture": 0.0,
        "health": 0.0,
        "education": 0.0,
        "water_sanitation": 0.0,
        "infrastructure": 0.0,
        "environment": 0.0,
        "mining": 0.0,
        "tribal_welfare": 0.0,
        "employment": 0.0,
        "urban_development": 0.0,
    }

    # Disaster-related signals
    disaster_terms = [
        "flood",
        "flooding",
        "drought",
        "lightning",
        "earthquake",
        "cyclone",
        "disaster",
        "emergency",
        "rescue",
        "relief",
    ]

    for term in disaster_terms:
        if term in text:
            context_scores["disaster_management"] += 0.15

    # Agriculture signals
    agriculture_terms = [
        "farmer",
        "farmers",
        "crop",
        "crops",
        "farming",
        "agriculture",
        "irrigation",
        "harvest",
    ]

    for term in agriculture_terms:
        if term in text:
            context_scores["agriculture"] += 0.15

    # Health signals
    health_terms = [
        "hospital",
        "doctor",
        "patient",
        "medicine",
        "healthcare",
        "health",
        "clinic",
        "disease",
    ]

    for term in health_terms:
        if term in text:
            context_scores["health"] += 0.15

    # Education signals
    education_terms = [
        "school",
        "student",
        "students",
        "teacher",
        "education",
        "classroom",
        "learning",
    ]

    for term in education_terms:
        if term in text:
            context_scores["education"] += 0.15

    # Water & sanitation signals
    water_terms = [
        "water",
        "drinking water",
        "sanitation",
        "toilet",
        "sewage",
        "wastewater",
        "water supply",
    ]

    for term in water_terms:
        if term in text:
            context_scores["water_sanitation"] += 0.15

    # Infrastructure signals
    infrastructure_terms = [
        "road",
        "roads",
        "bridge",
        "bridges",
        "infrastructure",
        "transport",
        "connectivity",
    ]

    for term in infrastructure_terms:
        if term in text:
            context_scores["infrastructure"] += 0.15

    # Environment signals
    environment_terms = [
        "pollution",
        "waste",
        "garbage",
        "forest",
        "forests",
        "climate",
        "environment",
        "deforestation",
    ]

    for term in environment_terms:
        if term in text:
            context_scores["environment"] += 0.15

    # Mining signals
    mining_terms = [
        "mine",
        "mining",
        "coal",
        "miner",
        "miners",
        "industrial",
        "chemical",
    ]

    for term in mining_terms:
        if term in text:
            context_scores["mining"] += 0.15

    # Tribal welfare signals
    tribal_terms = [
        "tribal",
        "tribes",
        "tribal community",
        "social welfare",
        "vulnerable community",
    ]

    for term in tribal_terms:
        if term in text:
            context_scores["tribal_welfare"] += 0.15

    # Employment signals
    employment_terms = [
        "job",
        "jobs",
        "employment",
        "unemployment",
        "skill",
        "skills",
        "training",
        "workforce",
    ]

    for term in employment_terms:
        if term in text:
            context_scores["employment"] += 0.15

    # Urban development signals
    urban_terms = [
        "urban",
        "city",
        "cities",
        "housing",
        "municipal",
        "traffic",
        "urbanization",
    ]

    for term in urban_terms:
        if term in text:
            context_scores["urban_development"] += 0.15

    # Combine semantic and contextual evidence.
    final_scores = {}

    for domain in context_scores:
        semantic_evidence = 0.0

        for prediction in semantic_result["top_predictions"]:
            if prediction["category"] == domain:
                semantic_evidence = prediction["score"]
                break

        final_scores[domain] = (
            0.7 * semantic_evidence
            + 0.3 * context_scores[domain]
        )

    ranked = sorted(
        final_scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    final_category = ranked[0][0]
    final_score = ranked[0][1]

    return {
        "category": final_category,
        "semantic_category": category,
        "semantic_score": round(semantic_score, 4),
        "context_score": round(
            context_scores[final_category],
            4
        ),
        "final_score": round(final_score, 4),
        "top_predictions": [
            {
                "category": domain,
                "score": round(score, 4)
            }
            for domain, score in ranked[:3]
        ],
    }