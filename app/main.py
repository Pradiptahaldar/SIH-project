from fastapi import FastAPI, UploadFile, File, Form, Query, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import os
import tempfile

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.ai.similarity.detector import detect_similarity, image_to_text
from app.processing.image import process_image
from app.processing.audio import process_audio
from app.ai.pipeline.analyzer import analyze_challenge

limiter = Limiter(key_func=get_remote_address)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp"
}

ALLOWED_AUDIO_TYPES = {
    "audio/mpeg",
    "audio/wav",
    "audio/x-wav",
    "audio/mp4",
    "audio/m4a",
    "audio/webm"
}
def validate_content_type(file: UploadFile, allowed_types: set[str]):
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

MAX_IMAGE_SIZE = 5 * 1024 * 1024
MAX_AUDIO_SIZE = 10 * 1024 * 1024
MAX_CHALLENGE_LENGTH = 5000

async def read_limited_file(file: UploadFile, max_size: int):
    data = await file.read(max_size + 1)

    if len(data) > max_size:
        raise ValueError("Uploaded file is too large")

    return data




app = FastAPI(
    title="SIH ai service",
    description="ai for sih 2026",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error"
        }
    )
app.state.limiter = limiter
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={
            "error": "Too many requests. Please try again later."
        }
    )

@app.get("/")
def root():
    return {"message": "ai service running"}

@app.post("/analyze")
@limiter.limit("10/minute")
async def analyze(
    request: Request,
    challenge: str = Query(..., min_length=1, max_length=MAX_CHALLENGE_LENGTH),
    image: UploadFile | None = File(None),
    audio: UploadFile | None = File(None)
):
    image_result = None
    audio_result = None

    if image:
        validate_content_type(image, ALLOWED_IMAGE_TYPES)
        image_data = await read_limited_file(image, MAX_IMAGE_SIZE)
        image_result = process_image(image_data)

    if audio:
        validate_content_type(audio, ALLOWED_AUDIO_TYPES)
        audio_data = await read_limited_file(audio, MAX_AUDIO_SIZE)

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
@limiter.limit("20/minute")
async def similarity(
    request: Request,
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
@limiter.limit("10/minute")
async def upload_image(request: Request,file: UploadFile = File(...)):
    validate_content_type(file, ALLOWED_IMAGE_TYPES)

    image_data = await read_limited_file(file, MAX_IMAGE_SIZE)
    image_info = process_image(image_data)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(image_data),
        "image": image_info
    }


@app.post("/upload-audio")
@limiter.limit("10/minute")
async def upload_audio(request: Request,file: UploadFile = File(...)):
    validate_content_type(file, ALLOWED_AUDIO_TYPES)

    audio_data = await read_limited_file(file, MAX_AUDIO_SIZE)

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