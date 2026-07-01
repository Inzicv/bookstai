'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  ['/', 'Accueil'],
  ['/books', 'Livres'],
  ['/review', 'Review'],
  ['/song', 'Song'],
  ['/social', 'Social'],
  ['/settings', 'Settings'],
]

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  return (
    <div className="min-h-screen text-slate-100">
      <header className="sticky top-0 z-10 border-b border-slate-800/90 bg-slate-950/85 backdrop-blur-xl">
        <div className="mx-auto flex max-w-6xl flex-col gap-4 px-4 py-4 sm:px-6 lg:flex-row lg:items-center lg:justify-between lg:px-8">
          <Link href="/" className="text-lg font-semibold tracking-tight text-slate-50">
            BookstAI
          </Link>
          <nav className="flex flex-wrap gap-2 text-sm">
            {links.map(([href, label]) => (
              <Link
                key={href}
                href={href}
                className={`rounded-full px-3 py-1.5 transition ${
                  pathname === href
                    ? 'bg-violet-500/20 text-violet-200 ring-1 ring-inset ring-violet-400/30'
                    : 'bg-slate-900/80 text-slate-300 hover:bg-slate-800 hover:text-slate-100'
                }`}
              >
                {label}
              </Link>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
    </div>
  )
}
