'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'

const links = [
  ['/', 'Accueil'],
  ['/review', 'Review'],
  ['/song', 'Song'],
  ['/hitl', 'HITL'],
  ['/learning', 'Learning'],
  ['/settings', 'Settings'],
]

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-10 border-b border-black/5 bg-[#f5f1ea]/90 backdrop-blur">
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-6 px-4 py-4 sm:px-6 lg:px-8">
          <Link href="/" className="text-lg font-semibold text-zinc-950">
            BookstAI
          </Link>
          <nav className="flex flex-wrap gap-2 text-sm">
            {links.map(([href, label]) => (
              <Link
                key={href}
                href={href}
                className={`rounded-full px-3 py-1.5 transition ${
                  pathname === href ? 'bg-zinc-950 text-white' : 'bg-white/70 text-zinc-700'
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

