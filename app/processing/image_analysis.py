from transformers import pipeline

image_classifier = pipeline(
    "zero-shot-image-classification",
    model="openai/clip-vit-base-patch32"
)

SIH_CATEGORIES = {
    "disaster_management": [
        "disaster",
        "flood",
        "drought",
        "cyclone",
        "earthquake",
        "fire",
        "emergency",
    ],
    "agriculture": [
        "farm",
        "farmer",
        "crop",
        "field",
        "farming",
        "irrigation",
        "harvest",
    ],
    "health": [
        "hospital",
        "doctor",
        "patient",
        "clinic",
        "medicine",
        "healthcare",
    ],
    "education": [
        "school",
        "classroom",
        "teacher",
        "student",
        "book",
        "computer",
        "education",
    ],
    "water_sanitation": [
        "river",
        "lake",
        "dam",
        "water",
        "drinking water",
        "sanitation",
        "toilet",
    ],
    "infrastructure": [
        "road",
        "bridge",
        "street",
        "transport",
        "building",
        "infrastructure",
    ],
    "environment": [
        "garbage",
        "waste",
        "pollution",
        "forest",
        "tree",
        "litter",
        "environment",
    ],
    "mining": [
        "mine",
        "mining",
        "miner",
        "industrial site",
        "factory",
        "industrial safety",
    ],
    "tribal_welfare": [
        "tribal community",
        "tribal village",
        "indigenous community",
        "community welfare",
    ],
    "employment": [
        "worker",
        "job",
        "employment",
        "skill training",
        "workplace",
        "livelihood",
    ],
    "urban_development": [
        "city",
        "urban area",
        "traffic",
        "building",
        "public transport",
        "housing",
    ],
    "energy": [
        "solar",
        "solar panel",
        "electricity",
        "power",
        "wind turbine",
        "renewable energy",
    ],
}
def analyze_image(image):
    relevance_labels = [
        "a photo related to a societal challenge involving disaster management, agriculture, health, education, water and sanitation, infrastructure, environment, mining, tribal welfare, employment, urban development, or energy",
        "a photo unrelated to any societal or community problem"
    ]
    relevance_results = image_classifier(
        image,
        candidate_labels=relevance_labels
    )
    relevant_label = relevance_results[0]["label"]
    relevance_confidence = relevance_results[0]["score"]
    is_relevant = (
        "related to a societal challenge" in relevant_label
        and relevance_confidence >= 0.60
    )

    if not is_relevant:
        return {
            "predictions": [],
            "category": "Unknown",
            "category_scores": {},
            "confidence": 0.0,
            "relevance": {
                "relevant": False,
                "confidence": relevance_confidence
            }
        }

    candidate_labels = [
        "a photo related to disaster management, floods, droughts, emergencies or disasters",
        "a photo related to agriculture, farming, crops, irrigation or farmers",
        "a photo related to health, healthcare, hospitals, doctors or medicine",
        "a photo related to education, schools, students, teachers or learning",
        "a photo related to water resources, drinking water or sanitation",
        "a photo related to roads, bridges, transport, buildings or infrastructure",
        "a photo related to environment, pollution, waste, forests or climate",
        "a photo related to mining, mines, industrial sites or industrial safety",
        "a photo related to tribal communities, tribal welfare or community development",
        "a photo related to employment, workers, jobs or skill development",
        "a photo related to urban development, cities, traffic, housing or public transport",
        "a photo related to energy, electricity, solar panels or renewable energy",
    ]

    results = image_classifier(
        image,
        candidate_labels=candidate_labels
    )

    label_to_category = {
        candidate_labels[0]: "disaster_management",
        candidate_labels[1]: "agriculture",
        candidate_labels[2]: "health",
        candidate_labels[3]: "education",
        candidate_labels[4]: "water_sanitation",
        candidate_labels[5]: "infrastructure",
        candidate_labels[6]: "environment",
        candidate_labels[7]: "mining",
        candidate_labels[8]: "tribal_welfare",
        candidate_labels[9]: "employment",
        candidate_labels[10]: "urban_development",
        candidate_labels[11]: "energy",
    }
    category_scores = {}
    for prediction in results:
        category = label_to_category[prediction["label"]]
        category_scores[category] = prediction["score"]

    best_prediction = results[0]

    best_category = label_to_category[best_prediction["label"]]
    confidence = best_prediction["score"]

    if confidence < 0.40:
        best_category = "Unknown"

    elif len(results) > 1:

        second_score = results[1]["score"]

        # If two categories are too close
        if confidence - second_score < 0.05:
            best_category = "Unknown"

    return {
        "predictions": results,
        "category": best_category,
        "category_scores": category_scores,
        "confidence": confidence,
        "relevance": {
            "relevant": True,
            "confidence": relevance_confidence
        }
    }