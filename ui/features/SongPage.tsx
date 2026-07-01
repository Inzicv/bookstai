'use client'

import { useState } from 'react'
import { runSong } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { ResultPanel } from '@/components/ResultPanel'
import { FormField } from '@/components/FormField'

export default function SongPage() {
  const [form, setForm] = useState({
    book_slug: 'alchemised',
    spoiler_mode: 'spoiler_free',
    prompt_type: 'video',
    platform: 'tiktok',
    provider: 'mock',
    image_backend: 'mock',
    hitl_enabled: true,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

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
          const response = await runSong(form)
          setLoading(false)
          if (!response.ok) {
            setError(response.error.message)
            return
          }
          setResult(response)
        }}
      >
        <FormField label="book_slug">
          <input className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500" value={form.book_slug} onChange={(e) => setForm({ ...form, book_slug: e.target.value })} />
        </FormField>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="spoiler_mode">
            <input className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500" value={form.spoiler_mode} onChange={(e) => setForm({ ...form, spoiler_mode: e.target.value })} />
          </FormField>
          <FormField label="prompt_type">
            <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.prompt_type} onChange={(e) => setForm({ ...form, prompt_type: e.target.value })}>
              <option value="character">character</option>
              <option value="scene">scene</option>
              <option value="thumbnail">thumbnail</option>
              <option value="video">video</option>
            </select>
          </FormField>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="platform">
            <input className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500" value={form.platform} onChange={(e) => setForm({ ...form, platform: e.target.value })} />
          </FormField>
          <FormField label="provider">
            <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.provider} onChange={(e) => setForm({ ...form, provider: e.target.value })}>
              <option value="mock">mock</option>
            </select>
          </FormField>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="image_backend">
            <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.image_backend} onChange={(e) => setForm({ ...form, image_backend: e.target.value })}>
              <option value="mock">mock</option>
            </select>
          </FormField>
          <label className="flex items-center gap-2 text-sm text-slate-300">
            <input type="checkbox" checked={form.hitl_enabled} onChange={(e) => setForm({ ...form, hitl_enabled: e.target.checked })} />
            HITL activé
          </label>
        </div>
        <LoadingButton loading={loading}>Générer Song</LoadingButton>
      </form>
      {error ? <ErrorMessage message={error} /> : null}
      {result ? <ResultPanel title="Résultat Song" data={result} /> : null}
    </div>
  )
}
