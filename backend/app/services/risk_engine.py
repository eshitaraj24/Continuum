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
