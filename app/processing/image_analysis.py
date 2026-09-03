from transformers import pipeline

image_classifier = pipeline(
    "zero-shot-image-classification",
    model="openai/clip-vit-base-patch32"
)

SIH_CATEGORIES = {
    "Education": [
        "school",
        "classroom",
        "teacher",
        "student",
        "book",
        "computer",
    ],
    "Agriculture": [
        "farm",
        "farmer",
        "crop",
        "field",
        "tractor",
        "harvest",
    ],
    "Healthcare": [
        "hospital",
        "doctor",
        "patient",
        "clinic",
        "medicine",
    ],
    "Water Resources": [
        "river",
        "lake",
        "water",
        "dam",
        "reservoir",
    ],
    "Environment": [
        "garbage",
        "waste",
        "pollution",
        "forest",
        "tree",
        "litter",
    ],
    "Energy": [
        "solar",
        "solar panel",
        "electricity",
        "power",
        "wind turbine",
    ],
    "Urban Development": [
        "road",
        "street",
        "traffic",
        "building",
        "bus",
        "bridge",
    ],
    "Accessibility": [
        "wheelchair",
        "ramp",
        "blind",
        "cane",
    ],
    "Public Administration": [
        "government",
        "office",
        "document",
        "official",
    ],
    "Rural Livelihoods": [
        "village",
        "rural",
        "worker",
        "market",
        "livelihood",
    ],
}
def analyze_image(image):
    relevance_labels = [
        "a photo related to a societal challenge involving education, agriculture, healthcare, water, environment, energy, cities, accessibility, government services, or rural livelihoods",
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
        "a photo related to education, schools, students or learning",
        "a photo related to agriculture, farming, crops or farmers",
        "a photo related to healthcare, hospitals, doctors or medicine",
        "a photo related to water resources, rivers, lakes, dams or water supply",
        "a photo related to environment, pollution, waste, forests or climate",
        "a photo related to energy, electricity, solar panels or renewable energy",
        "a photo related to urban development, roads, traffic, transport or cities",
        "a photo related to accessibility, disability, wheelchairs or ramps",
        "a photo related to public administration, government services or public offices",
        "a photo related to rural livelihoods, villages, rural workers or rural employment",
    ]

    results = image_classifier(
        image,
        candidate_labels=candidate_labels
    )

    label_to_category = {
        candidate_labels[0]: "Education",
        candidate_labels[1]: "Agriculture",
        candidate_labels[2]: "Healthcare",
        candidate_labels[3]: "Water Resources",
        candidate_labels[4]: "Environment",
        candidate_labels[5]: "Energy",
        candidate_labels[6]: "Urban Development",
        candidate_labels[7]: "Accessibility",
        candidate_labels[8]: "Public Administration",
        candidate_labels[9]: "Rural Livelihoods",
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