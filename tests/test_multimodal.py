from app.ai.multimodal.fusion import (
    fuse_multimodal,
    build_unified_text
)


text_result = "Farmers are facing crop losses due to poor irrigation."

image_result = {
    "analysis": {
        "relevant": True,
        "category": "agriculture",
        "confidence": 0.91
    }
}

audio_result = {
    "text": "The irrigation system is not working properly."
}


result = fuse_multimodal(
    text_result=text_result,
    image_result=image_result,
    audio_result=audio_result
)

print("\n========== MULTIMODAL FUSION ==========\n")
print(result)


unified_text = build_unified_text(
    text_result=text_result,
    image_result=image_result,
    audio_result=audio_result
)

print("\n========== UNIFIED TEXT ==========\n")
print(unified_text)