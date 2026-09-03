from app.ai.extraction.extractor import extract_problem
from app.ai.priority.scorer import calculate_priority


tests = [
    (
        "Farmers in rural villages are struggling with crop losses due to poor irrigation and unpredictable rainfall.",
        "agriculture"
    ),
    (
        "Villagers have to travel long distances to access healthcare because nearby hospitals lack adequate medical facilities.",
        "health"
    ),
    (
        "Coal mine workers are exposed to dangerous conditions due to inadequate safety equipment.",
        "mining"
    ),
    (
        "Many students in rural areas do not have access to quality digital education.",
        "education"
    )
]


for challenge, category in tests:

    extracted = extract_problem(challenge)

    result = calculate_priority(
        problem=extracted["problem"],
        category=category,
        affected_group=extracted["affected_group"],
        location=extracted["location"],
        causes=extracted["causes"],
        impact=extracted["impact"]
    )

    print("\nChallenge:")
    print(challenge)

    print("\nExtracted:")
    print(extracted)

    print("\nPriority:")
    print(result)