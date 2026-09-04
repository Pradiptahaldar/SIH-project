from fastapi import FastAPI, UploadFile, File, Form
import os
import tempfile
from app.ai.similarity.detector import detect_similarity, image_to_text

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

        suffix = os.path.splitext(audio.filename or "")[1]

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(audio_data)
            audio_path = temp_file.name

        try:
            audio_result = process_audio(audio_path)
        finally:
            os.unlink(audio_path)

    return analyze_challenge(
        challenge=challenge,
        image_result=image_result,
        audio_result=audio_result
    )
@app.post("/similarity")
async def similarity(
    challenge: str | None = Form(None),
    existing_challenges: str = Form(...),
    image: UploadFile | None = File(None)
):
    if existing_challenges:
        existing_list = [
            item.strip()
            for item in existing_challenges.split(",")
            if item.strip()
        ]
    else:
        existing_list = []

    similarity_text = challenge

    if image:
        image_data = await image.read()
        image_result = process_image(image_data)
        similarity_text = image_to_text(image_result)

    if not similarity_text:
        return {
            "error": "Challenge text or image is required"
        }

    return detect_similarity(
        challenge=similarity_text,
        existing_challenges=existing_list
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

    suffix = os.path.splitext(file.filename or "")[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
        temp_file.write(audio_data)
        audio_path = temp_file.name

    try:
        result = process_audio(audio_path)
    finally:
        os.unlink(audio_path)
   
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(audio_data),
        "audio": result
    }