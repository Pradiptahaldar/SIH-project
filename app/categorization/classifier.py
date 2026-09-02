CATEGORIES = {
    "Education": {
        "digital education": 3,
        "online learning": 3,
        "school": 1,
        "student": 1,
        "education": 2,
        "teacher": 1,
        "college": 1,
        "university": 1,
        "learning": 1,
        "classroom": 1,
    },
    "Healthcare": {
        "healthcare": 3,
        "health care": 3,
        "hospital": 2,
        "medical": 2,"medicine": 2,
        "doctor": 1,
        "patient": 1,
        "clinic": 1,
        "health": 1,
    },
    "Agriculture": {
        "agriculture": 3,
        "farming": 3,
        "farmer": 2,"crop": 2,
        "fertilizer": 2,"harvest": 2,
        "irrigation": 1,
    },
    "Water Resources": {
        "water resources": 3,
        "drinking water": 3,"water supply": 3,
        "groundwater": 2,"river": 2,"lake": 2,"water": 1,
        "irrigation": 1,
    },
    "Environment": {"environment": 2,
        "pollution": 3,
        "air quality": 3,
        "deforestation": 3,
        "forest": 2,
        "climate": 2,
        "waste": 2,
    },
    "Energy": {
        "renewable energy": 3,
        "renewable": 2,
        "electricity": 2,
        "solar": 2,
        "power": 2,
        "energy": 2,
        "grid": 1,
    },
    "Urban Development": {
        "urban development": 3,
        "traffic": 2,
        "drainage": 2,
        "transport": 2,
        "city": 1,
        "urban": 2,
        "road": 1,
        "street": 1,
    },
    "Accessibility": {
        "accessibility": 3,
        "wheelchair": 3,
        "disability": 3,
        "disabled": 2,
        "blind": 2,
        "deaf": 2,
        "mobility": 2,
        "accessible": 2,
    },
    "Public Administration": {
        "public administration": 3,
        "public service": 3,
        "government": 2,
        "municipality": 2,
        "administration": 2,
        "citizen": 1,
        "official": 1,
        "document": 1,
    },
    "Rural Livelihoods": {
        "rural livelihoods": 3,
        "rural employment": 3,
        "livelihood": 3,
        "rural": 2,
        "village": 2,
        "employment": 2,
        "self employment": 2,
        "income": 1,
    },
}
def classify_challenge(challenge: str) -> str:
    text = challenge.lower()
    scores = {}
    for category, keywords in CATEGORIES.items():
        score = 0
        for keyword, weight in keywords.items():
            if keyword in text:
                score += weight
        scores[category] = score
    best_score= max(scores.values())
    total_score= sum(scores.values())
    if best_score==0:
        return "Unknown" , scores, 0.0
    confidence= best_score/ total_score
    top_categories=[category
                    for category, score in scores.items()
                    if score == best_score
                    ]
    best_category= top_categories[0]
    return best_category, scores, confidence
    
