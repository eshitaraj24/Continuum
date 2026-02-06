"""
seed_dummy_data.py = optional CLI script for inspecting the seeded dataset.

Run:
  python -m app.data.seed_dummy_data

This prints what is currently in store.py after seeding.
"""

from app.data.store import seed_dummy_data, get_patients, get_latest_checkin


def print_triage_table():
    print("\nRECOVERY MONITORING PORTAL (SEEDED DUMMY DATA)\n")

    for p in get_patients():
        c = get_latest_checkin(p["id"])
        if not c:
            continue

        alerts_str = ", ".join(c["alerts"]) if c["alerts"] else "None"

        print(
            f"{p['name']} | Day {p['post_op_day']} | {p['surgery']} | "
            f"Risk {c['risk']} | {c['status']} | Alerts: {alerts_str}"
        )


if __name__ == "__main__":
    seed_dummy_data()
    print_triage_table()
