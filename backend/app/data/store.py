"""
store.py = in-memory data store for the running API.

Why this exists:
- FastAPI routes need stable data across requests
- Seed data should be generated once and reused
- Later we can swap this with a real database layer
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import random
import uuid

from ..services.risk_engine import compute_risk


def uid() -> str:
    return str(uuid.uuid4())


# Single source of truth (runtime memory)
PATIENTS: List[Dict[str, Any]] = []
CHECKINS_BY_PATIENT: Dict[str, List[Dict[str, Any]]] = {}


def seed_dummy_data() -> None:
    """
    Populate PATIENTS and CHECKINS_BY_PATIENT once.
    Call this ONCE at server startup.
    """
    global PATIENTS, CHECKINS_BY_PATIENT

    PATIENTS = [
        {"id": uid(), "name": "Sarah Johnson", "surgery": "Total Knee Replacement", "post_op_day": 3},
        {"id": uid(), "name": "Robert Wilson", "surgery": "Hip Replacement", "post_op_day": 2},
        {"id": uid(), "name": "Michael Chen", "surgery": "ACL Reconstruction", "post_op_day": 14},
        {"id": uid(), "name": "Lisa Martinez", "surgery": "Total Knee Replacement", "post_op_day": 9},
        {"id": uid(), "name": "John Smith", "surgery": "Rotator Cuff Repair", "post_op_day": 7},
        {"id": uid(), "name": "Emily Davis", "surgery": "Spinal Fusion", "post_op_day": 5},
    ]

    CHECKINS_BY_PATIENT = {}
    now = datetime.now()

    for p in PATIENTS:
        temp = random.choice([98.6, 99.5, 101.2, 102.4])
        pain = random.choice([3, 5, 7, 9])
        symptoms = {
            "drainage": random.choice([False, False, True]),
            "swelling": random.choice([False, True]),
        }

        risk, status, alerts = compute_risk(temp, pain, symptoms, p["post_op_day"])

        checkin = {
            "created_at": now.isoformat(),
            "last_checkin_minutes": random.randint(5, 180),
            "temp_f": temp,
            "pain": pain,
            "symptoms": symptoms,
            "risk": risk,
            "status": status,
            "alerts": alerts,
        }

        CHECKINS_BY_PATIENT[p["id"]] = [checkin]


def get_patients() -> List[Dict[str, Any]]:
    return PATIENTS


def get_latest_checkin(patient_id: str) -> Optional[Dict[str, Any]]:
    arr = CHECKINS_BY_PATIENT.get(patient_id, [])
    return arr[0] if arr else None
