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
        setState({ loading: false, ok: true, message: `${data.app} · ${data.mode}` })
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
          state.ok ? 'bg-emerald-400' : state.ok === false ? 'bg-rose-400' : 'bg-amber-400'
        }`}
      />
      <span className="font-medium text-slate-100">
        {state.loading ? 'API en cours...' : state.ok ? 'API disponible' : 'API indisponible'}
      </span>
      <span className="text-slate-400">{state.message}</span>
    </div>
  )
}
