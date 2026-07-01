'use client'

import { useEffect, useState } from 'react'
import { getApiBaseUrl, getHealth } from '@/lib/api'

export function ApiStatus() {
  const [state, setState] = useState<{ loading: boolean; ok: boolean | null; message: string }>({
    loading: true,
    ok: null,
    message: `Vérification de l'API sur ${getApiBaseUrl()}...`,
  })

  useEffect(() => {
    let mounted = true
    getHealth()
      .then((data) => {
        if (!mounted) return
        setState({ loading: false, ok: true, message: `${data.app} · ${data.mode} · ${getApiBaseUrl()}` })
      })
      .catch((error) => {
        if (!mounted) return
        setState({ loading: false, ok: false, message: error.message })
      })
    return () => {
      mounted = false
    }
  }, [])

  return (
    <div className="panel inline-flex max-w-full flex-wrap items-center gap-3 rounded-full px-4 py-2 text-sm">
      <span
        className={`h-2.5 w-2.5 rounded-full ${
          state.ok ? 'bg-emerald-500' : state.ok === false ? 'bg-rose-500' : 'bg-amber-500'
        }`}
      />
      <span className="font-medium">
        {state.loading ? 'API en cours...' : state.ok ? 'API disponible' : 'API indisponible'}
      </span>
      <span className="text-zinc-600">{state.message}</span>
    </div>
  )
}
