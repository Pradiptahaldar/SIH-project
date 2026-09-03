CATEGORIES = {
    "disaster_management": {
        "label": "Disaster Management",
        "keywords": {
            "disaster": 3,
            "disaster management": 4,
            "emergency": 3,
            "flood": 3,
            "drought": 3,
            "lightning": 3,
            "fire": 2,
            "road accident": 3,
            "accident": 2,
            "rescue": 2,
            "relief": 2,
            "emergency response": 4,
            "natural disaster": 4,
        }
    },

    "agriculture": {
        "label": "Agriculture & Food Security",
        "keywords": {
            "agriculture": 3,
            "farming": 3,
            "farmer": 3,
            "farmers": 3,
            "crop": 2,
            "crops": 2,
            "food security": 4,
            "fertilizer": 2,
            "harvest": 2,
            "irrigation": 2,
            "soil": 2,
            "seeds": 2,
            "seed": 2,
            "pesticide": 2,
            "livestock": 2,
            "cultivation": 2,
            "agricultural": 3,
        }
    },

    "health": {
        "label": "Health & Medical",
        "keywords": {
            "health": 2,
            "healthcare": 3,
            "health care": 3,
            "medical": 3,
            "medicine": 3,
            "hospital": 3,
            "doctor": 2,
            "patient": 2,
            "clinic": 2,
            "disease": 2,
            "treatment": 2,
            "diagnosis": 2,
            "ambulance": 3,
            "maternal health": 4,
            "child health": 4,
        }
    },

    "education": {
        "label": "Education",
        "keywords": {
            "education": 3,
            "digital education": 4,
            "online learning": 4,
            "school": 2,
            "student": 2,
            "students": 2,
            "teacher": 2,
            "teachers": 2,
            "college": 2,
            "university": 2,
            "learning": 2,
            "classroom": 2,
            "literacy": 2,
            "teaching": 2,
            "school infrastructure": 4,
        }
    },

    "water_sanitation": {
        "label": "Water & Sanitation",
        "keywords": {
            "water": 2,
            "water supply": 4,
            "drinking water": 4,
            "tap water": 4,
            "sanitation": 4,
            "sewage": 3,
            "sewerage": 3,
            "groundwater": 3,
            "water shortage": 4,
            "water scarcity": 4,
            "clean water": 4,
            "toilet": 2,
            "wastewater": 3,
            "irrigation": 1,
        }
    },

    "infrastructure": {
        "label": "Roads & Infrastructure",
        "keywords": {
            "infrastructure": 4,
            "road": 3,
            "roads": 3,
            "bridge": 3,
            "highway": 3,
            "street": 2,
            "road connectivity": 4,
            "transport infrastructure": 4,
            "public infrastructure": 4,
            "construction": 2,
            "building": 1,
        }
    },

    "environment": {
        "label": "Environment & Forest",
        "keywords": {
            "environment": 3,
            "environmental": 3,
            "pollution": 4,
            "air pollution": 4,
            "air quality": 4,
            "water pollution": 4,
            "deforestation": 4,
            "forest": 3,
            "forests": 3,
            "forest fire": 4,
            "climate": 3,
            "climate change": 4,
            "waste": 2,
            "plastic waste": 4,
            "biodiversity": 3,
            "ecosystem": 3,
        }
    },

    "mining": {
        "label": "Mining & Industrial Safety",
        "keywords": {
            "mining": 4,
            "mine": 3,
            "miner": 3,
            "coal mining": 4,
            "coal mine": 4,
            "mining accident": 5,
            "mine accident": 5,
            "industrial": 3,
            "industrial accident": 5,
            "industrial safety": 5,
            "chemical accident": 5,
            "mines": 3,
            "coalfield": 3,
            "land subsidence": 4,
        }
    },

    "tribal_welfare": {
        "label": "Tribal & Social Welfare",
        "keywords": {
            "tribal": 4,
            "tribal welfare": 5,
            "tribal community": 4,
            "tribal communities": 4,
            "scheduled tribe": 4,
            "scheduled tribes": 4,
            "social welfare": 4,
            "social inclusion": 3,
            "welfare": 2,
            "marginalized": 3,
            "marginalised": 3,
            "vulnerable community": 3,
            "vulnerable communities": 3,
        }
    },

    "employment": {
        "label": "Employment & Skill Development",
        "keywords": {
            "employment": 3,
            "unemployment": 4,
            "job": 2,
            "jobs": 2,
            "employment opportunity": 4,
            "employment opportunities": 4,
            "skill development": 5,
            "vocational training": 4,
            "skill training": 4,
            "training": 2,
            "livelihood": 3,
            "livelihoods": 3,
            "self employment": 4,
            "self-employment": 4,
            "workforce": 3,
            "career": 2,
            "income": 2,
        }
    },

    "urban_development": {
        "label": "Urban Development & Housing",
        "keywords": {
            "urban": 3,
            "urban development": 5,
            "urbanization": 4,
            "urbanisation": 4,
            "city": 2,
            "cities": 2,
            "housing": 4,
            "urban housing": 5,
            "municipal": 3,
            "municipality": 3,
            "drainage": 3,
            "urban drainage": 5,
            "traffic": 3,
            "public transport": 3,
            "smart city": 4,
            "unplanned growth": 4,
        }
    },

    "other": {
        "label": "Other",
        "keywords": {}
    }
}
def classify_challenge(challenge: str):
    text = challenge.lower()
    scores = {}
    for category, data in CATEGORIES.items():
        score = 0
        for keyword, weight in data["keywords"].items():
            if keyword in text:
                score += weight
        scores[category] = score
    best_score = max(scores.values())
    if best_score == 0:
        return "other", scores, 0.0
    total_score = sum(scores.values())
    confidence = best_score / total_score
    top_categories = [
        category
        for category, score in scores.items()
        if score == best_score
    ]
    best_category = top_categories[0]
    return best_category, scores, confidence