# Stores discharge instructions + default tasks per surgery type

# backend/app/data/recovery_plans.py

from typing import Dict, Any

RECOVERY_PLANS_BY_SURGERY: Dict[str, Dict[str, Any]] = {
    "Total Knee Replacement": {
        "instructions": [
            {"title": "Pain control", "body": "Take prescribed meds as directed. Do not exceed daily limits. Call if pain suddenly worsens."},
            {"title": "Wound care", "body": "Keep incision clean and dry. Do not scrub. Watch for drainage, spreading redness, or foul odor."},
            {"title": "Activity", "body": "Walk short distances several times daily. Follow PT guidance. Avoid twisting/pivoting early."},
            {"title": "Red flags", "body": "Seek care for fever ≥ 102F, uncontrolled pain, pus-like drainage, chest pain, or shortness of breath."},
        ],
        "default_tasks": [
            {"id": "meds_am", "label": "Take morning pain medication (if prescribed)", "frequency": "daily"},
            {"id": "walk_1", "label": "Short walk (5–10 min)", "frequency": "daily"},
            {"id": "wound_check", "label": "Check incision for redness/swelling/drainage", "frequency": "daily"},
            {"id": "checkin", "label": "Daily recovery check-in", "frequency": "daily"},
        ],
    },

    "Hip Replacement": {
        "instructions": [
            {"title": "Movement precautions", "body": "Follow surgeon precautions to avoid dislocation. Use assistive devices as recommended."},
            {"title": "Wound care", "body": "Keep incision clean and dry. Monitor for drainage or increasing redness."},
            {"title": "Red flags", "body": "Seek care for fever ≥ 102F, severe pain, new drainage, chest pain, or shortness of breath."},
        ],
        "default_tasks": [
            {"id": "meds_am", "label": "Take morning pain medication (if prescribed)", "frequency": "daily"},
            {"id": "walk_1", "label": "Short walk (5–10 min)", "frequency": "daily"},
            {"id": "wound_check", "label": "Check incision for changes", "frequency": "daily"},
            {"id": "checkin", "label": "Daily recovery check-in", "frequency": "daily"},
        ],
    },

    # Add postpartum / C-section next once this structure works
}


def get_recovery_plan(surgery: str) -> Dict[str, Any]: # Default general surgery instructions (if we don't have data yet)
    # fallback so you always have something even if surgery type is new
    return RECOVERY_PLANS_BY_SURGERY.get(surgery, {
        "instructions": [
            {"title": "General recovery", "body": "Follow your discharge paperwork. If symptoms worsen or you feel unsafe, contact your care team."},
            {"title": "Red flags", "body": "Seek care for high fever, uncontrolled pain, heavy bleeding, pus-like drainage, chest pain, or shortness of breath."},
        ],
        "default_tasks": [
            {"id": "checkin", "label": "Daily recovery check-in", "frequency": "daily"},
        ],
    })
