'use client'

import { useEffect, useState } from 'react'
import { runSong } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'
import { BookSelect } from '@/components/BookSelect'

type SongFormState = {
  book_slug: string
  story_scope: 'pitch_only' | 'full_spoilers'
  song_style: 'parody'
  platform: 'tiktok' | 'instagram'
  provider: 'mock' | 'openai'
  model: string | null
  temperature: string
  hitl_enabled: boolean
}

type Provider = 'mock' | 'openai'
type OpenAIModel = 'gpt-5.5' | 'gpt-5.4' | 'gpt-5.4-mini' | 'gpt-5.4-nano'

const OPENAI_MODEL_OPTIONS: Array<{ value: OpenAIModel; label: string }> = [
  { value: 'gpt-5.5', label: 'GPT-5.5 — meilleur choix qualité / raisonnement' },
  { value: 'gpt-5.4', label: 'GPT-5.4 — bon équilibre qualité / coût' },
  { value: 'gpt-5.4-mini', label: 'GPT-5.4 mini — plus rapide et moins cher' },
  { value: 'gpt-5.4-nano', label: 'GPT-5.4 nano — économique pour tests simples' },
]

function getFriendlyErrorMessage(code: string, message: string) {
  if (code === 'MISSING_API_KEY') {
    return 'Clé OpenAI manquante côté backend. Configure OPENAI_API_KEY puis relance l’API.'
  }
  if (code === 'OPENAI_DEPENDENCY_MISSING') {
    return 'La dépendance OpenAI n’est pas installée côté backend. Installe l’extra openai du projet.'
  }
  if (code === 'INVALID_PROVIDER') {
    return 'Provider invalide. Choisis mock ou openai.'
  }
  return message
}

export default function SongPage() {
  const [form, setForm] = useState<SongFormState>({
    book_slug: 'alchemised',
    story_scope: 'pitch_only',
    song_style: 'parody',
    provider: 'mock' as Provider,
    model: null,
    temperature: '0.7',
    hitl_enabled: true,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (form.provider === 'openai' && !form.model) {
      setForm((current) => ({ ...current, model: 'gpt-5.4-mini' }))
    }
    if (form.provider === 'mock' && form.model !== null) {
      setForm((current) => ({ ...current, model: null }))
    }
  }, [form.model, form.provider])

  const workflow = result?.result

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold text-slate-100">Song</h1>
      <form
        className="panel grid gap-4 rounded-3xl p-6"
        onSubmit={async (event) => {
          event.preventDefault()
          setLoading(true)
          setError(null)
          setResult(null)
          const response = await runSong({
            book_slug: form.book_slug,
            story_scope: form.story_scope,
            song_style: form.song_style,
            provider: form.provider,
            model: form.provider === 'openai' ? form.model : null,
            temperature: Number(form.temperature),
            hitl_enabled: form.hitl_enabled,
          })
          setLoading(false)
          if (!response.ok) {
            setError(getFriendlyErrorMessage(response.error.code, response.error.message))
            return
          }
          setResult(response)
        }}
        >
        <BookSelect value={form.book_slug} onChange={(book_slug) => setForm({ ...form, book_slug })} />
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Portée de l’histoire">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.story_scope}
              onChange={(e) =>
                setForm({ ...form, story_scope: e.target.value as SongFormState['story_scope'] })
              }
            >
              <option value="pitch_only">Pitch / 4e de couverture seulement</option>
              <option value="full_spoilers">Livre complet avec spoilers</option>
            </select>
          </FormField>
          <FormField label="Style de chanson">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.song_style}
              onChange={(e) =>
                setForm({ ...form, song_style: e.target.value as SongFormState['song_style'] })
              }
            >
              <option value="parody">Parodie</option>
            </select>
          </FormField>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Provider texte">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.provider}
              onChange={(e) => setForm({ ...form, provider: e.target.value as Provider })}
            >
              <option value="mock">Mock — test local sans coût</option>
              <option value="openai">OpenAI — génération texte réelle</option>
            </select>
            <p className="text-xs text-slate-400">
              La clé OpenAI est lue côté backend depuis{' '}
              <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-100">
                OPENAI_API_KEY
              </code>
              . Elle ne doit jamais être saisie ici.
            </p>
          </FormField>
        </div>
        {form.provider === 'openai' ? (
          <div className="grid gap-4 md:grid-cols-2">
            <FormField label="Modèle OpenAI">
              <select
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
                value={form.model ?? 'gpt-5.4-mini'}
                onChange={(e) => setForm({ ...form, model: e.target.value as OpenAIModel })}
              >
                {OPENAI_MODEL_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <p className="text-xs text-slate-400">
                Pour commencer, utilise GPT-5.4 mini : bon compromis entre qualité, vitesse et coût.
              </p>
            </FormField>
            <FormField label="Température">
              <input
                type="number"
                step="0.1"
                className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
                value={form.temperature}
                onChange={(e) => setForm({ ...form, temperature: e.target.value })}
              />
            </FormField>
          </div>
        ) : (
          <div className="rounded-2xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm text-slate-300">
            Le provider mock n’utilise pas de vrai modèle.
          </div>
        )}
        <label className="flex items-center gap-2 text-sm text-slate-300">
          <input
            type="checkbox"
            checked={form.hitl_enabled}
            onChange={(e) => setForm({ ...form, hitl_enabled: e.target.checked })}
          />
          HITL activé
        </label>
        <LoadingButton loading={loading}>Générer Song</LoadingButton>
      </form>
      {error ? <ErrorMessage message={error} /> : null}
      {result ? (
        <section className="panel space-y-4 rounded-3xl p-6">
          <h2 className="text-lg font-semibold text-slate-50">Propositions de chanson</h2>
          <div className="whitespace-pre-wrap text-slate-200">{workflow?.song?.response ?? workflow?.song_final ?? ''}</div>
          <details className="rounded-2xl border border-slate-800 bg-slate-950 p-4">
            <summary className="cursor-pointer text-sm text-slate-300">Voir les détails techniques</summary>
            <pre className="mt-3 overflow-auto text-xs text-slate-300">{JSON.stringify(result, null, 2)}</pre>
          </details>
        </section>
      ) : null}
    </div>
  )
}
