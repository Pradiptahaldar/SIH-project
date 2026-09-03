def fuse_multimodal(
    text_result=None,
    image_result=None,
    audio_result=None
):
    """
    Combine information from text, image, and audio inputs
    into a single multimodal understanding.
    """

    sources = []
    combined_information = []

    # Text
    if text_result:
        sources.append("text")

        if isinstance(text_result, str):
            combined_information.append(text_result)

    # Image
    if image_result:
        sources.append("image")

        if isinstance(image_result, dict):
            analysis = image_result.get("analysis")

            if analysis:
                combined_information.append(
                    f"Visual evidence: {analysis}"
                )

    # Audio
    if audio_result:
        sources.append("audio")

        if isinstance(audio_result, dict):
            audio_text = audio_result.get("text")

            if audio_text:
                combined_information.append(
                    audio_text
                )

    return {
        "sources": sources,
        "combined_information": combined_information,
        "source_count": len(sources)
    }


def build_unified_text(
    text_result=None,
    image_result=None,
    audio_result=None
):
    """
    Build a single text representation from multimodal inputs.
    """

    parts = []

    # Original text
    if text_result:
        if isinstance(text_result, str):
            parts.append(text_result)

    # Image information
    if image_result and isinstance(image_result, dict):
        analysis = image_result.get("analysis")

        if analysis:
            if isinstance(analysis, dict):
                category = analysis.get("category")

                if category:
                    parts.append(
                        f"Visual evidence indicates {category}."
                    )
            else:
                parts.append(
                    f"Visual evidence: {analysis}"
                )

    # Audio transcription
    if audio_result and isinstance(audio_result, dict):
        audio_text = audio_result.get("text")

        if audio_text:
            parts.append(audio_text)

    return " ".join(parts)