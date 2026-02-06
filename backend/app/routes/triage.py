from fastapi import APIRouter
from ..data.store import get_patients, get_latest_checkin

router = APIRouter()

@router.get("/triage")
def get_triage_dashboard():
    dashboard = []

    for p in get_patients():
        c = get_latest_checkin(p["id"])
        if not c:
            continue

        dashboard.append({
            "patient_id": p["id"],
            "name": p["name"],
            "surgery": p["surgery"],
            "post_op_day": p["post_op_day"],
            "last_checkin_minutes": c["last_checkin_minutes"],
            "temp_f": c["temp_f"],
            "pain": c["pain"],
            "risk": c["risk"],
            "status": c["status"],
            "alerts": c["alerts"],
        })

    # Sort: Critical first, then Monitor, then Stable; then by risk desc
    rank = {"Critical": 0, "Monitor": 1, "Stable": 2}
    dashboard.sort(key=lambda row: (rank.get(row["status"], 99), -row["risk"]))

    return dashboard
