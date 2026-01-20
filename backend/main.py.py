from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import analyze_alert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlertRequest(BaseModel):
    alert_text: str

@app.post("/analyze")
async def analyze(request: AlertRequest):
    return await analyze_alert(request.alert_text)
