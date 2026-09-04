from app.ai.pipeline.analyzer import analyze_challenge

challenge = (
    "Farmers in rural villages are facing crop losses."
)

image_result = {
    "analysis": {
        "relevant": True,
        "category": "Agriculture",
        "confidence": 0.91
    }
}

audio_result = {
    "text": (
        "The irrigation system is not working properly."
    )
}

result = analyze_challenge(
    challenge=challenge,
    image_result=image_result,
    audio_result=audio_result
)

print("\n========== MULTIMODAL PIPELINE ==========\n")

print("UNIFIED TEXT:")
print(result["unified_text"])

print("\nCATEGORY:")
print(result["category"])

print("\nEXTRACTION:")
print(result["extraction"])

print("\nPRIORITY:")
print(result["priority"])

print("\nSIMILARITY:")
print(result["similarity"])

print("\nEXPLANATION:")
print(result["explanation"])