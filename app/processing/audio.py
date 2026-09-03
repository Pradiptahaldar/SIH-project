import whisper
model = whisper.load_model("base")
def process_audio(audio_path: str):
    result = model.transcribe(audio_path, language="en")
    return {
        "text": result["text"].strip()
    }