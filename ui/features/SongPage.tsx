'use client'

import { useState } from 'react'
import { runSong } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { JsonBlock } from '@/components/JsonBlock'
import { FormField } from '@/components/FormField'

type SongFormState = {
  book_slug: string
  story_scope: 'pitch_only' | 'full_spoilers'
  song_style: 'parody'
  reference_song: string
  platform: string
  provider: 'mock'
  model: string
  temperature: string
  hitl_enabled: boolean
}

export default function SongPage() {
  const [form, setForm] = useState<SongFormState>({
    book_slug: 'alchemised',
    story_scope: 'pitch_only',
    song_style: 'parody',
    reference_song: '',
    platform: 'tiktok',
    provider: 'mock',
    model: '',
    temperature: '0.7',
    hitl_enabled: true,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  const workflow = result?.result

  const sections = [
    ['Contexte utilisé', workflow?.context],
    ['Comedy room', workflow?.comedy],
    ['Chanson', workflow?.song],
    ['Storyboard', workflow?.storyboard],
    ['Prompts personnages', workflow?.prompts?.character_prompts],
    ['Prompts backgrounds', workflow?.prompts?.background_prompts],
    ['Prompts objets', workflow?.prompts?.prop_prompts],
    ['Social', workflow?.social],
  ] as const

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
            reference_song: form.reference_song,
            platform: form.platform,
            provider: form.provider,
            model: form.model || null,
            temperature: Number(form.temperature),
            hitl_enabled: form.hitl_enabled,
          })
          setLoading(false)
          if (!response.ok) {
            setError(response.error.message)
            return
          }
          setResult(response)
        }}
      >
        <FormField label="Livre">
          <input
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
            value={form.book_slug}
            onChange={(e) => setForm({ ...form, book_slug: e.target.value })}
          />
        </FormField>
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
        <FormField label="Chanson de référence">
          <input
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
            value={form.reference_song}
            onChange={(e) => setForm({ ...form, reference_song: e.target.value })}
            placeholder="Mockingbird - Eminem"
          />
        </FormField>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Plateforme">
            <input
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
              value={form.platform}
              onChange={(e) => setForm({ ...form, platform: e.target.value })}
            />
          </FormField>
          <FormField label="Provider">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.provider}
              onChange={(e) => setForm({ ...form, provider: e.target.value as 'mock' })}
            >
              <option value="mock">mock</option>
            </select>
          </FormField>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Température">
            <input
              type="number"
              step="0.1"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
              value={form.temperature}
              onChange={(e) => setForm({ ...form, temperature: e.target.value })}
            />
          </FormField>
          <label className="flex items-center gap-2 text-sm text-slate-300">
            <input
              type="checkbox"
              checked={form.hitl_enabled}
              onChange={(e) => setForm({ ...form, hitl_enabled: e.target.checked })}
            />
            HITL activé
          </label>
        </div>
        <LoadingButton loading={loading}>Générer Song</LoadingButton>
      </form>
      {error ? <ErrorMessage message={error} /> : null}
      {result ? (
        <section className="space-y-4">
          <div className="grid gap-4 lg:grid-cols-2">
            {sections.map(([label, value]) => (
              <div key={label} className="panel rounded-3xl p-5">
                <div className="text-xs uppercase tracking-[0.18em] text-slate-400">{label}</div>
                <div className="mt-3">
                  <JsonBlock value={value ?? {}} />
                </div>
              </div>
            ))}
          </div>
          {result?.hitl ? (
            <div className="panel rounded-3xl p-5">
              <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Session HITL</div>
              <div className="mt-3">
                <JsonBlock value={result.hitl} />
              </div>
            </div>
          ) : null}
          {result?.hitl_session_path ? (
            <div className="panel rounded-3xl p-5 text-slate-300">
              Session HITL: <span className="text-slate-100">{result.hitl_session_path}</span>
            </div>
          ) : null}
          <details className="panel rounded-3xl p-5">
            <summary className="cursor-pointer text-sm font-medium text-slate-200">
              Debug JSON complet
            </summary>
            <div className="mt-4">
              <JsonBlock value={result} />
            </div>
          </details>
        </section>
      ) : null}
    </div>
  )
}
