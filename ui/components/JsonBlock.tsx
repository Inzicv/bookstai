export function JsonBlock({ value }: { value: unknown }) {
  return (
    <pre className="overflow-auto rounded-2xl border border-slate-800 bg-slate-950 p-4 text-xs leading-6 text-slate-100">
      {JSON.stringify(value, null, 2)}
    </pre>
  )
}
