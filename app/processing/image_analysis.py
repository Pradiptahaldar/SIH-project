from transformers import pipeline
image_classifier= pipeline("image-classification",
                           model= "google/vit-base-patch16-224")

def analyze_image(image):
    results = image_classifier(image)
    category_scores = {
        category: 0
        for category in SIH_CATEGORIES
    }
    for prediction in results:
        label = prediction["label"].lower()
        score = prediction["score"]
        for category, keywords in SIH_CATEGORIES.items():
            for keyword in keywords:
                if keyword in label:
                    category_scores[category] += score
    best_category = max(
        category_scores,
        key=category_scores.get
    )
    if category_scores[best_category] == 0:
        best_category = "Unknown"
    return {
        "predictions": results[:5],
        "category": best_category,
        "category_scores": category_scores
    }
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
        "wheelchair","ramp",
        "blind","cane",
    ],
    "Public Administration": [
        "government","office",
        "document","official",
    ],
    "Rural Livelihoods": ["village","rural",
        "worker","market","livelihood",
    ],
}