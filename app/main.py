from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.categorization.classifier import classify_challenge
from app.processing.image import process_image
app= FastAPI(title= "SIH ai service",
             description="ai for sih 2026",
             version= "1.0.0")
class ChallengeRequest(BaseModel):
    challenge:str
    #image:str | None=None
    #audio:str | None=None
    #video:str | None=None
@app.get("/")
def root():
    return {"message": "ai service running"}
@app.post("/categorize")
def categorize(request: ChallengeRequest):
    category, scores, confidence = classify_challenge(request.challenge)

    return {"category": category,
            "scores": scores,
            "confidence": confidence}
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