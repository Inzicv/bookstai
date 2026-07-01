import Link from 'next/link'
import { ApiStatus } from '@/components/ApiStatus'

const shortcuts = [
  { href: '/review', label: 'Review' },
  { href: '/song', label: 'Song' },
  { href: '/hitl', label: 'HITL' },
  { href: '/learning', label: 'Learning' },
]

export default function HomePage() {
  return (
    <div className="space-y-8">
      <section className="space-y-4">
        <p className="text-sm uppercase tracking-[0.3em] text-slate-400">Studio local</p>
        <h1 className="text-4xl font-semibold tracking-tight text-slate-100 sm:text-6xl">BookstAI</h1>
        <p className="max-w-2xl text-base text-slate-300 sm:text-lg">
          Une application web locale pour piloter BookstAI dans le navigateur, avec FastAPI en
          arrière-plan.
        </p>
      </section>

      <ApiStatus />

      <section className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {shortcuts.map((item) => (
          <Link
            key={item.href}
            href={item.href}
            className="panel rounded-2xl px-5 py-4 transition hover:-translate-y-0.5 hover:shadow-lg"
          >
            <div className="text-sm text-slate-400">Accès rapide</div>
            <div className="mt-1 text-lg font-medium text-slate-100">{item.label}</div>
          </Link>
        ))}
      </section>
    </div>
  )
}
