export function JsonBlock({ value }: { value: unknown }) {
  return <pre className="overflow-auto rounded-2xl bg-zinc-950 p-4 text-xs text-zinc-100">{JSON.stringify(value, null, 2)}</pre>
}

