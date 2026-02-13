from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import triage
from .data.store import seed_dummy_data

app = FastAPI(title="Continuum Clinician API")

# --- CORS (required for frontend on localhost:5173 - Vite default port) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Seed dummy data once on startup ---
seed_dummy_data()

# --- Routes ---
app.include_router(triage.router)

@app.get("/")
def health():
    return {"status": "ok"}
