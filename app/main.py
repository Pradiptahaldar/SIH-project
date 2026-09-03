from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from app.processing.text import process_text
from app.processing.image import process_image
from app.processing.audio import process_audio
from app.ai.pipeline.analyzer import analyze_challenge


app = FastAPI(
    title="SIH ai service",
    description="ai for sih 2026",
    version="1.0.0"
)


class ChallengeRequest(BaseModel):
    challenge: str
    # image: str | None = None
    # audio: str | None = None
    # video: str | None = None


@app.get("/")
def root():
    return {"message": "ai service running"}


@app.post("/categorize")
def categorize(request: ChallengeRequest):
    return process_text(request.challenge)


@app.post("/analyze")
def analyze(request: ChallengeRequest):
    return analyze_challenge(request.challenge)


@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    image_data = await file.read()
    image_info = process_image(image_data)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(image_data),
        "image": image_info
    }


@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    audio_data = await file.read()
    audio_path = f"temp_{file.filename}"

    with open(audio_path, "wb") as f:
        f.write(audio_data)

    result = process_audio(audio_path)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(audio_data),
        "audio": result
    }