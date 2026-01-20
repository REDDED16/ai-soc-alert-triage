from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from orchestrator import analyze_alert

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze(payload: dict):
    return await analyze_alert(payload.get("alert_text", ""))

@app.get("/")
def root():
    return {"status": "Backend running"}
