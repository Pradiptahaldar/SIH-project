from fastapi import FastAPI
from pydantic import BaseModel
from app.categorization.classifier import classify_challenge
app= FastAPI(title= "SIH ai service",
             description="ai for sih 2026",
             version= "1.0.0")
class ChallengeRequest(BaseModel):
    challenge:str
@app.get("/")
def root():
    return {"message": "ai service running"}
@app.post("/categorize")
def categorize(request: ChallengeRequest):
    category = classify_challenge(request.challenge)

    return {"catefory": category}