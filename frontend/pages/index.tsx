import { useEffect, useState } from "react";

type Patient = {
  patient_id: string;
  name: string;
  surgery: string;
  post_op_day: number;
  last_checkin_minutes: number;
  temp_f: number;
  pain: number;
  risk: number;
  status: "Stable" | "Monitor" | "Critical";
  alerts: string[];
};

export default function Dashboard() {
  // IMPORTANT: must start as an array
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/triage")
      .then((res) => res.json())
      .then((data) => {
        console.log("API response:", data);

        if (Array.isArray(data)) {
          // Sort by risk (highest first)
          data.sort((a, b) => b.risk - a.risk);
          setPatients(data);
        } else {
          setPatients([]);
        }

        setLoading(false);
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setPatients([]);
        setLoading(false);
      });
  }, []);

  return (
    <main className="min-h-screen bg-slate-50 px-8 py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold text-slate-800">
          Clinician Recovery Dashboard
        </h1>
        <p className="text-sm text-slate-500">
          Post-discharge patient triage (prototype)
        </p>
      </header>

      {loading ? (
        <p className="text-slate-500">Loading patients…</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {Array.isArray(patients) &&
            patients.map((p) => (
              <PatientCard key={p.patient_id} patient={p} />
            ))}
        </div>
      )}
    </main>
  );
}

function PatientCard({ patient }: { patient: Patient }) {
  const riskColor =
    patient.risk >= 70
      ? "text-red-600"
      : patient.risk >= 35
      ? "text-yellow-600"
      : "text-green-600";

  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4">
      <div className="flex items-start justify-between mb-2">
        <div>
          <h2 className="font-medium text-slate-800">{patient.name}</h2>
          <p className="text-xs text-slate-500">{patient.surgery}</p>
        </div>
        <StatusBadge status={patient.status} />
      </div>

      <div className="text-sm text-slate-700 space-y-1">
        <p>Post-op day: {patient.post_op_day}</p>
        <p>Last check-in: {patient.last_checkin_minutes} min ago</p>
        <p>Temperature: {patient.temp_f}°F</p>
        <p>Pain: {patient.pain}/10</p>
        <p className="font-medium">
          Risk score: <span className={riskColor}>{patient.risk}</span>
        </p>
      </div>

      {patient.alerts.length > 0 && (
        <div className="mt-3 rounded-md bg-red-50 border border-red-200 p-2 text-xs text-red-700">
          ⚠ {patient.alerts.join(", ")}
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const styles: Record<string, string> = {
    Stable: "bg-green-100 text-green-700",
    Monitor: "bg-yellow-100 text-yellow-800",
    Critical: "bg-red-100 text-red-700",
  };

  return (
    <span
      className={`text-xs font-medium px-2 py-1 rounded-full ${styles[status]}`}
    >
      {status}
    </span>
  );
}
