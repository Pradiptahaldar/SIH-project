from app.ai.semantic.classifier import classify_semantic
from app.ai.extraction.extractor import extract_problem
from app.ai.priority.scorer import calculate_priority
from app.ai.similarity.detector import detect_similarity
from app.ai.explanation.generator import generate_explanation
from app.ai.multimodal.fusion import build_unified_text


def analyze_challenge(
    challenge: str,
    existing_challenges: list | None = None,
    image_result=None,
    audio_result=None
):
    if not challenge or not challenge.strip():
        return {"error": "Challenge text cannot be empty"}

    # Build unified text from available modalities
    unified_text = build_unified_text(
        text_result=challenge,
        image_result=image_result,
        audio_result=audio_result
    )

    # Semantic classification
    category_result = classify_semantic(unified_text)

    # Problem extraction
    extraction_result = extract_problem(challenge)

    # Priority calculation
    priority_result = calculate_priority(
        problem=extraction_result["problem"],
        category=category_result["category"],
        affected_group=extraction_result["affected_group"],
        location=extraction_result["location"],
        causes=extraction_result["causes"],
        impact=extraction_result["impact"]
    )

    # Explanation
    explanation_result = generate_explanation(
        challenge=unified_text,
        category=category_result,
        extraction=extraction_result,
        priority=priority_result
    )

    # Similarity
    similarity_result = detect_similarity(
        unified_text,
        existing_challenges or []
    )

    return {
        "challenge": challenge,
        "unified_text": unified_text,
        "category": category_result,
        "extraction": extraction_result,
        "priority": priority_result,
        "similarity": similarity_result,
        "explanation": explanation_result
    }