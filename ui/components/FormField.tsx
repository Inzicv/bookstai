export function FormField({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="grid gap-2 text-sm font-medium text-slate-300">
      <span className="text-xs uppercase tracking-[0.18em] text-slate-400">{label}</span>
      {children}
    </label>
  )
}
