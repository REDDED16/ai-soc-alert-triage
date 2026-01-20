from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.orchestrator import analyze_alert
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # IMPORTANT for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlertRequest(BaseModel):
    alert_text: str

@app.post("/analyze")
async def analyze(request: AlertRequest):
    return await analyze_alert(request.alert_text)
