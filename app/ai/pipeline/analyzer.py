from app.ai.semantic.classifier import classify_semantic
from app.ai.extraction.extractor import extract_problem
from app.ai.priority.scorer import calculate_priority
from app.ai.similarity.detector import detect_similarity


def analyze_challenge(challenge: str, existing_challenges: list | None = None):

    if not challenge or not challenge.strip():
        return {
            "error": "Challenge text cannot be empty"
        }

    # 1. Categorization
    category_result = classify_semantic(challenge)

    # 2. Problem extraction
    extraction_result = extract_problem(challenge)

    # 3. Priority scoring
    priority_result = calculate_priority(
        problem=extraction_result["problem"],
        category=category_result["category"],
        affected_group=extraction_result["affected_group"],
        location=extraction_result["location"],
        causes=extraction_result["causes"],
        impact=extraction_result["impact"]
    )

    # 4. Similarity / duplicate detection
    similarity_result = detect_similarity(
        challenge,
        existing_challenges or []
    )

    return {
        "challenge": challenge,
        "category": category_result,
        "extraction": extraction_result,
        "priority": priority_result,
        "similarity": similarity_result
    }