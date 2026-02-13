import { ReactNode } from "react";

type LayoutProps = {
  children: ReactNode;
};

export function Layout({ children }: LayoutProps) {
  return (
    <div className="app-shell">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl bg-teal-500/90 shadow-sm" />
            <div>
              <p className="text-sm font-semibold text-slate-900">
                Continuum
              </p>
              <p className="text-xs text-slate-500">Clinician Triage Console</p>
            </div>
          </div>
          <div className="hidden text-xs text-slate-500 sm:block">
            Demo data • Read-only • Not for clinical use
          </div>
        </div>
      </header>

      <main className="app-main">
        <div className="mx-auto max-w-6xl px-4 py-6 sm:px-6 lg:px-8">
          {children}
        </div>
      </main>
    </div>
  );
}

