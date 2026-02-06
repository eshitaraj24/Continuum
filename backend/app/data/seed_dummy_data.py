from datetime import datetime, timedelta
import random
import uuid

def uid():
    return str(uuid.uuid4())

patients = [
    {
        "id": uid(),
        "name": "Sarah Johnson",
        "surgery": "Total Knee Replacement",
        "post_op_day": 3,
    },
    {
        "id": uid(),
        "name": "Robert Wilson",
        "surgery": "Hip Replacement",
        "post_op_day": 2,
    },
    {
        "id": uid(),
        "name": "Michael Chen",
        "surgery": "ACL Reconstruction",
        "post_op_day": 14,
    },
    {
        "id": uid(),
        "name": "Lisa Martinez",
        "surgery": "Total Knee Replacement",
        "post_op_day": 9,
    },
    {
        "id": uid(),
        "name": "John Smith",
        "surgery": "Rotator Cuff Repair",
        "post_op_day": 7,
    },
    {
        "id": uid(),
        "name": "Emily Davis",
        "surgery": "Spinal Fusion",
        "post_op_day": 5,
    },
]

def compute_risk(temp_f, pain, symptoms, post_op_day):
    score = 0
    alerts = []

    if temp_f >= 102:
        score += 40
        alerts.append("High fever")

    if pain >= 9:
        score += 25
        alerts.append("Severe pain")

    if symptoms.get("drainage"):
        score += 20
        alerts.append("Drainage noted")

    if symptoms.get("swelling"):
        score += 15
        alerts.append("Worsening swelling")

    if post_op_day <= 3:
        score += 10

    if score >= 70:
        status = "Critical"
    elif score >= 35:
        status = "Monitor"
    else:
        status = "Stable"

    return score, status, alerts


checkins = []

now = datetime.now()

for p in patients:
    temp = random.choice([98.6, 99.5, 101.2, 102.4])
    pain = random.choice([3, 5, 7, 9])
    symptoms = {
        "drainage": random.choice([False, False, True]),
        "swelling": random.choice([False, True]),
    }

    risk, status, alerts = compute_risk(
        temp, pain, symptoms, p["post_op_day"]
    )

    checkins.append({
        "patient_id": p["id"],
        "last_activity": (now - timedelta(minutes=random.randint(10, 180))).strftime("%H:%M"),
        "temp_f": temp,
        "pain": pain,
        "risk": risk,
        "status": status,
        "alerts": alerts,
    })


def print_triage_table():
    print("\nRECOVERY MONITORING PORTAL (DUMMY DATA)\n")
    for p, c in zip(patients, checkins):
        print(
            f"{p['name']} | Day {p['post_op_day']} | {p['surgery']} | "
            f"Risk {c['risk']} | {c['status']} | Alerts: {', '.join(c['alerts']) or 'None'}"
        )


if __name__ == "__main__":
    print_triage_table()
