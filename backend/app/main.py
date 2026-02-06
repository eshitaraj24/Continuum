from fastapi import FastAPI
from .routes import triage
from .data.store import seed_dummy_data

app = FastAPI(title="Continuum Clinician API")

# Seed once when the server starts
seed_dummy_data()

app.include_router(triage.router)

@app.get("/")
def health():
    return {"status": "ok"}
