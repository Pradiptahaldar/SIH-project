from fastapi import FastAPI
app= FastAPI(title= "SIH ai service",
             description="ai for sih 2026",
             version= "1.0.0")
@app.get("/")
def root():
    return {"message": "ai service running"}