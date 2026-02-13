import { useEffect, useMemo, useState } from "react";
import { Layout } from "./components/Layout";
import { PatientCard } from "./components/PatientCard";
import type { PatientTriage } from "./types";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [patients, setPatients] = useState<PatientTriage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [criticalOnly, setCriticalOnly] = useState(false);

  useEffect(() => {
    // Simple read-only fetch of triage data
    fetch(`${API_BASE}/triage`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        return res.json();
      })
      .then((data) => {
        const list = Array.isArray(data) ? (data as PatientTriage[]) : [];
        // Backend already sorts by status + risk, but ensure risk ordering as a fallback
        list.sort((a, b) => b.risk - a.risk);
        setPatients(list);
        setError(null);
      })
      .catch((err: unknown) => {
        console.error("Failed to load triage data", err);
        setError(err instanceof Error ? err.message : "Unknown error");
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const filtered = useMemo(() => {
    let result = patients;

    if (criticalOnly) {
      result = result.filter((p) => p.status === "Critical");
    }

    const q = query.trim().toLowerCase();
    if (q.length > 0) {
      result = result.filter((p) => {
        const nameMatch = p.name.toLowerCase().includes(q);
        const surgeryMatch = p.surgery.toLowerCase().includes(q);
        const dayMatch = String(p.post_op_day).includes(q);
        return nameMatch || surgeryMatch || dayMatch;
      });
    }

    return result;
  }, [patients, criticalOnly, query]);

  const stats = useMemo(() => {
    const total = patients.length;
    const critical = patients.filter((p) => p.status === "Critical").length;
    const monitor = patients.filter((p) => p.status === "Monitor").length;
    const stable = patients.filter((p) => p.status === "Stable").length;
    return { total, critical, monitor, stable };
  }, [patients]);

  return (
    <Layout>
      <section aria-labelledby="dashboard-heading" className="space-y-6">
        <header className="space-y-2">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h1
                id="dashboard-heading"
                className="text-2xl font-semibold tracking-tight text-slate-900 sm:text-3xl"
              >
                Triage Dashboard
              </h1>
              <p className="mt-1 text-sm text-slate-600">
                Ranked list of post-discharge patients by computed risk score.
              </p>
            </div>

            <div className="flex flex-wrap items-center gap-3">
              <span className="inline-flex items-center gap-1 rounded-full bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                Live connection to API
              </span>
            </div>
          </div>
        </header>

        {/* Overview stats */}
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <StatCard label="Total" value={stats.total} tone="neutral" />
          <StatCard label="Critical" value={stats.critical} tone="critical" />
          <StatCard label="Monitor" value={stats.monitor} tone="monitor" />
          <StatCard label="Stable" value={stats.stable} tone="stable" />
        </div>

        {/* Controls */}
        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div className="relative w-full sm:max-w-sm">
            <span className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-400">
              <svg
                className="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </span>
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search by name, surgery, or day…"
              className="w-full rounded-lg border border-slate-300 bg-white py-2.5 pl-9 pr-3 text-sm text-slate-900 placeholder:text-slate-400 focus:border-teal-500 focus:outline-none focus:ring-2 focus:ring-teal-100"
            />
          </div>

          <button
            type="button"
            onClick={() => setCriticalOnly((v) => !v)}
            className={`inline-flex min-h-[40px] items-center justify-center rounded-lg px-4 text-sm font-medium transition ${
              criticalOnly
                ? "border border-red-300 bg-red-50 text-red-700 hover:bg-red-100"
                : "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50"
            }`}
          >
            {criticalOnly ? "Showing critical only" : "Filter: Critical only"}
          </button>
        </div>

        {/* Content states */}
        {loading ? (
          <div className="flex items-center justify-center py-16">
            <div className="text-center">
              <div className="mx-auto h-10 w-10 animate-spin rounded-full border-4 border-slate-200 border-t-teal-500" />
              <p className="mt-4 text-sm text-slate-500">Loading patients…</p>
            </div>
          </div>
        ) : error ? (
          <div className="rounded-xl border border-red-200 bg-red-50 p-6 text-sm text-red-700">
            <p className="font-semibold">Unable to load triage data</p>
            <p className="mt-1 text-red-600">{error}</p>
          </div>
        ) : filtered.length === 0 ? (
          <div className="rounded-xl border border-slate-200 bg-white p-6 text-center text-sm text-slate-600">
            {criticalOnly || query
              ? "No patients match the current filters."
              : "No patients available in the triage list."}
          </div>
        ) : (
          <div className="space-y-3">
            {filtered.map((patient) => (
              <PatientCard key={patient.patient_id} patient={patient} />
            ))}
          </div>
        )}
      </section>
    </Layout>
  );
}

type StatCardProps = {
  label: string;
  value: number;
  tone: "neutral" | "critical" | "monitor" | "stable";
};

function StatCard({ label, value, tone }: StatCardProps) {
  const toneStyles: Record<StatCardProps["tone"], string> = {
    neutral: "bg-white border-slate-200 text-slate-800",
    critical: "bg-red-50 border-red-200 text-red-700",
    monitor: "bg-amber-50 border-amber-200 text-amber-700",
    stable: "bg-teal-50 border-teal-200 text-teal-700"
  };

  return (
    <div
      className={`rounded-xl border px-3 py-3 text-sm shadow-sm ${toneStyles[tone]}`}
    >
      <p className="text-xs font-medium uppercase tracking-wide text-slate-500">
        {label}
      </p>
      <p className="mt-1 text-xl font-semibold">{value}</p>
    </div>
  );
}

