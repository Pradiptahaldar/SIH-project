from app.ai.pipeline.analyzer import analyze_challenge


challenge = (
    "Farmers in rural villages are struggling with crop losses "
    "due to poor irrigation and unpredictable rainfall."
)

existing_challenges = [
    "Farmers are suffering because irrigation facilities are inadequate.",
    "Students in rural areas lack access to digital education.",
    "Coal mine workers face dangerous working conditions."
]


result = analyze_challenge(
    challenge,
    existing_challenges
)

print("\n========== COMPLETE ANALYSIS ==========\n")

print("CATEGORY:")
print(result["category"])

print("\nEXTRACTION:")
print(result["extraction"])

print("\nPRIORITY:")
print(result["priority"])

print("\nSIMILARITY:")
print(result["similarity"])