from fastapi import APIRouter
from datetime import datetime, timedelta
import random
import uuid
from app.services.risk_engine import compute_risk

router = APIRouter()

def uid():
    return str(uuid.uuid4())

PATIENTS = [
    {"id": uid(), "name": "Sarah Johnson", "surgery": "Total Knee Replacement", "post_op_day": 3},
    {"id": uid(), "name": "Robert Wilson", "surgery": "Hip Replacement", "post_op_day": 2},
    {"id": uid(), "name": "Michael Chen", "surgery": "ACL Reconstruction", "post_op_day": 14},
]

@router.get("/triage")
def get_triage_dashboard():
    now = datetime.now()
    dashboard = []

    for p in PATIENTS:
        temp = random.choice([98.6, 99.5, 101.2, 102.4])
        pain = random.choice([3, 5, 7, 9])
        symptoms = {
            "drainage": random.choice([False, True]),
            "swelling": random.choice([False, True]),
        }

        risk, status, alerts = compute_risk(
            temp, pain, symptoms, p["post_op_day"]
        )

        dashboard.append({
            "patient_id": p["id"],
            "name": p["name"],
            "surgery": p["surgery"],
            "post_op_day": p["post_op_day"],
            "last_checkin_minutes": random.randint(5, 180),
            "temp_f": temp,
            "pain": pain,
            "risk": risk,
            "status": status,
            "alerts": alerts,
        })

    return dashboard
