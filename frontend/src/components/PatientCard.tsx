import { PatientTriage } from "../types";
import { StatusBadge } from "./StatusBadge";

type PatientCardProps = {
  patient: PatientTriage;
};

export function PatientCard({ patient }: PatientCardProps) {
  const riskLevel =
    patient.risk >= 70
      ? { label: "High", color: "text-red-600", pill: "bg-red-50 border-red-200" }
      : patient.risk >= 35
      ? { label: "Moderate", color: "text-amber-600", pill: "bg-amber-50 border-amber-200" }
      : { label: "Low", color: "text-teal-600", pill: "bg-teal-50 border-teal-200" };

  return (
    <article className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm transition hover:border-teal-300 hover:shadow-md">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <h2 className="truncate text-base font-semibold text-slate-900">
              {patient.name}
            </h2>
            <span className="rounded-full bg-slate-50 px-2 py-0.5 text-[11px] font-mono text-slate-500">
              {patient.patient_id.slice(0, 8)}
            </span>
          </div>
          <p className="mt-1 text-sm text-slate-600">
            {patient.surgery} • Post-op day {patient.post_op_day}
          </p>
          <p className="mt-1 text-xs text-slate-500">
            Last check-in:{" "}
            <span className="font-medium text-slate-700">
              {patient.last_checkin_minutes}m
            </span>{" "}
            ago
          </p>
        </div>

        <div className="flex flex-col items-end gap-2 sm:items-end">
          <StatusBadge status={patient.status} />
          <div
            className={`inline-flex items-baseline gap-2 rounded-full border px-3 py-1 text-xs font-medium ${riskLevel.pill}`}
          >
            <span className="uppercase tracking-wide text-slate-500">
              Risk
            </span>
            <span className={`text-lg font-semibold ${riskLevel.color}`}>
              {patient.risk}
            </span>
            <span className="text-[11px] text-slate-400">/100</span>
          </div>
        </div>
      </div>

      <div className="mt-4 grid grid-cols-3 gap-2 text-xs sm:text-sm">
        <Metric label="Temperature" value={`${patient.temp_f}°F`} />
        <Metric label="Pain" value={`${patient.pain}/10`} />
        <Metric label="Alerts" value={patient.alerts.length ? `${patient.alerts.length}` : "None"} />
      </div>

      {patient.alerts.length > 0 && (
        <div className="mt-3 rounded-lg border border-red-100 bg-red-50 px-3 py-2">
          <p className="text-xs font-semibold text-red-700">Alerts</p>
          <p className="mt-1 text-xs text-red-700">
            {patient.alerts.join(" • ")}
          </p>
        </div>
      )}
    </article>
  );
}

type MetricProps = {
  label: string;
  value: string;
};

function Metric({ label, value }: MetricProps) {
  return (
    <div className="rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-2">
      <p className="text-[11px] text-slate-500">{label}</p>
      <p className="mt-0.5 text-sm font-semibold text-slate-900">{value}</p>
    </div>
  );
}

