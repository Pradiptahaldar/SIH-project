CATEGORIES = {
    "Education": ["school","student","education","teacher","college",
        "university","learning","classroom","digital education",
    ],
    "Healthcare": ["hospital","health","healthcare","doctor",
        "medicine","medical","clinic","patient",
    ],
    "Agriculture": ["farmer","farming","agriculture","crop",
        "irrigation","fertilizer","harvest",
    ],
    "Water Resources": ["water","drinking water","river","lake",
        "groundwater","water supply","irrigation",
    ],
    "Environment": ["pollution","waste","environment","forest",
        "deforestation","climate","air quality",
    ],
    "Energy": ["electricity","energy","power",
               "solar","grid","renewable",
    ],
    "Urban Development": ["city","urban","traffic","road",
        "street","drainage","transport",
    ],
    "Accessibility": ["disability","disabled","wheelchair","accessible",
        "blind","deaf","mobility",
    ],
    "Public Administration": [
        "government","municipality","public service","administration",
        "citizen","official","document",
    ],
    "Rural Livelihoods": [
        "rural","village","livelihood","employment",
        "self employment","income","rural employment",
    ],
}


def classify_challenge(challenge: str) -> str:
    text = challenge.lower()
    scores = {}

    for category, keywords in CATEGORIES.items():
        score = 0
        for keyword in keywords:
            if keyword in text:
                score += 1
        scores[category] = score
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        return "Unknown"
    return best_category