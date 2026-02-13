// Inferred from FastAPI /triage backend
export type TriageStatus = "Stable" | "Monitor" | "Critical";

export type PatientTriage = {
  patient_id: string;
  name: string;
  surgery: string;
  post_op_day: number;
  last_checkin_minutes: number;
  temp_f: number;
  pain: number;
  risk: number; // 0–100
  status: TriageStatus;
  alerts: string[];
};

// Assumption: there is a single latest check-in driving these fields; no free-text notes are present in the API.

