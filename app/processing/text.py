from app.categorization.classifier import classify_challenge
def process_text(challenge: str):
    if not challenge or not challenge.strip():
        return {
            "category": "Unknown",
            "scores": {},
            "confidence": 0.0
        }
    category, scores, confidence = classify_challenge(challenge)
    return {
        "category": category,
        "scores": scores,
        "confidence": confidence
    }