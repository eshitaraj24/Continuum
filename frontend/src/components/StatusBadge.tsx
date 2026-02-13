import { TriageStatus } from "../types";

type StatusBadgeProps = {
  status: TriageStatus;
};

export function StatusBadge({ status }: StatusBadgeProps) {
  const styles: Record<TriageStatus, string> = {
    Stable: "bg-teal-50 text-teal-700 border-teal-300",
    Monitor: "bg-amber-50 text-amber-700 border-amber-300",
    Critical: "bg-red-50 text-red-700 border-red-300"
  };

  return (
    <span
      className={`inline-flex items-center rounded-full border px-3 py-1 text-xs font-semibold uppercase tracking-wide ${styles[status]}`}
    >
      {status}
    </span>
  );
}

