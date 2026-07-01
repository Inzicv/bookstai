import { JsonBlock } from './JsonBlock'

export function ResultPanel({ title, data }: { title: string; data: unknown }) {
  return (
    <section className="panel space-y-4 rounded-3xl p-6">
      <h2 className="text-lg font-semibold">{title}</h2>
      <JsonBlock value={data} />
    </section>
  )
}

