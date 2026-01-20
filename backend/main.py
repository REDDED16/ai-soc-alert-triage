from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import analyze_alert
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AlertRequest(BaseModel):
    alert_text: str

@app.post("/analyze")
async def analyze(req: AlertRequest):
    return await analyze_alert(req.alert_text)
