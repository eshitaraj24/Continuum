from fastapi import APIRouter, HTTPException
from ..data.store import get_patient, get_latest_checkin, append_checkin
from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime
from ..services.risk_engine import compute_risk
from ..data.recovery_plans import get_recovery_plan

class SymptomPayload(BaseModel):
    drainage: Optional[bool] = None
    swelling: Optional[bool] = None

class CheckinPayload(BaseModel):
    temp_f: Optional[float] = None
    pain: Optional[int] = None
    symptoms: Optional[SymptomPayload] = None


router = APIRouter(prefix="/patient", tags=["patient"])

@router.get("/{patient_id}")
def get_patient_summary(patient_id: str):
    p = get_patient(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    c = get_latest_checkin(patient_id)

    # In MVP, days_since_surgery = post_op_day (same thing for now)
    summary = {
        "patient_id": p["id"],
        "name": p["name"],
        "surgery": p["surgery"],
        "post_op_day": p["post_op_day"],
        "days_since_surgery": p["post_op_day"],
    }

    # If no check-in exists yet, return patient info only
    if not c:
        summary.update({
            "last_checkin_minutes": None,
            "risk": None,
            "status": "No check-in yet",
            "alerts": [],
        })
        return summary

    summary.update({
        "last_checkin_minutes": c["last_checkin_minutes"],
        "risk": c["risk"],
        "status": c["status"],
        "alerts": c["alerts"],
    })
    return summary

@router.post("/{patient_id}/checkin")
def submit_checkin(patient_id: str, payload: CheckinPayload):
    p = get_patient(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Allow partial input: fill missing values with safe defaults for MVP
    temp_f = payload.temp_f if payload.temp_f is not None else 98.6
    pain = payload.pain if payload.pain is not None else 0

    symptoms_dict = {
        "drainage": False,
        "swelling": False,
    }
    if payload.symptoms is not None:
        if payload.symptoms.drainage is not None:
            symptoms_dict["drainage"] = payload.symptoms.drainage
        if payload.symptoms.swelling is not None:
            symptoms_dict["swelling"] = payload.symptoms.swelling

    risk, status, alerts = compute_risk(temp_f, pain, symptoms_dict, p["post_op_day"])

    checkin = {
        "created_at": datetime.now().isoformat(),
        "last_checkin_minutes": 0,  # just checked in
        "temp_f": temp_f,
        "pain": pain,
        "symptoms": symptoms_dict,
        "risk": risk,
        "status": status,
        "alerts": alerts,
    }

    append_checkin(patient_id, checkin)

    return {
        "patient_id": patient_id,
        "risk": risk,
        "status": status,
        "alerts": alerts,
        "guidance": guidance_for_status(status),
    }


def guidance_for_status(status: str) -> str:
    if status == "Critical":
        return "Seek medical attention now (call your care team or go to urgent/ER)."
    if status == "Monitor":
        return "Monitor closely. If symptoms worsen or you feel concerned, contact your care team."
    if status == "Stable":
        return "You’re on track. Continue your recovery plan and check in daily."
    return "Thanks for checking in."


@router.get("/{patient_id}/plan")
def get_patient_plan(patient_id: str):
    p = get_patient(patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")

    plan = get_recovery_plan(p["surgery"])

    return {
        "patient_id": p["id"],
        "name": p["name"],
        "surgery": p["surgery"],
        "post_op_day": p["post_op_day"],
        "instructions": plan["instructions"],
        "tasks": plan["default_tasks"],
    }
