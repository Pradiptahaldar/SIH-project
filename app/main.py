from fastapi import FastAPI, UploadFile, File

from app.processing.image import process_image
from app.processing.audio import process_audio
from app.ai.pipeline.analyzer import analyze_challenge


app = FastAPI(
    title="SIH ai service",
    description="ai for sih 2026",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "ai service running"}

@app.post("/analyze")
async def analyze(
    challenge: str,
    image: UploadFile | None = File(None),
    audio: UploadFile | None = File(None)
):
    image_result = None
    audio_result = None

    if image:
        image_data = await image.read()
        image_result = process_image(image_data)

    if audio:
        audio_data = await audio.read()
        audio_path = f"temp_{audio.filename}"

        with open(audio_path, "wb") as f:
            f.write(audio_data)

        audio_result = process_audio(audio_path)

    return analyze_challenge(
        challenge=challenge,
        image_result=image_result,
        audio_result=audio_result
    )


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