from fastapi import FastAPI
from app.routes import triage

app = FastAPI(title="Continuum Clinician API")

app.include_router(triage.router)

@app.get("/")
def health():
    return {"status": "ok"}
