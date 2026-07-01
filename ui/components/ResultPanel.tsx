import { JsonBlock } from './JsonBlock'

export function ResultPanel({ title, data }: { title: string; data: unknown }) {
  return (
    <section className="panel space-y-4 rounded-3xl p-6">
      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold text-slate-50">{title}</h2>
      </div>
      <JsonBlock value={data} />
    </section>
  )
}
