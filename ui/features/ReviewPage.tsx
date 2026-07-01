'use client'

import { useState } from 'react'
import { runReview } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { ResultPanel } from '@/components/ResultPanel'
import { FormField } from '@/components/FormField'

export default function ReviewPage() {
  const [form, setForm] = useState({
    book_slug: 'alchemised',
    user_opinion: '',
    platform: 'tiktok',
    provider: 'mock',
    model: '',
    temperature: '0.7',
    hitl_enabled: true,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold text-slate-100">Review</h1>
      <form
        className="panel grid gap-4 rounded-3xl p-6"
        onSubmit={async (event) => {
          event.preventDefault()
          setLoading(true)
          setError(null)
          setResult(null)
          const response = await runReview({
            ...form,
            temperature: Number(form.temperature),
            model: form.model || null,
          })
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
        <FormField label="user_opinion">
          <textarea className="min-h-32 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500" value={form.user_opinion} onChange={(e) => setForm({ ...form, user_opinion: e.target.value })} />
        </FormField>
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
          <FormField label="model">
            <input className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500" value={form.model} onChange={(e) => setForm({ ...form, model: e.target.value })} />
          </FormField>
          <FormField label="temperature">
            <input type="number" step="0.1" className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500" value={form.temperature} onChange={(e) => setForm({ ...form, temperature: e.target.value })} />
          </FormField>
        </div>
        <label className="flex items-center gap-2 text-sm text-slate-300">
          <input type="checkbox" checked={form.hitl_enabled} onChange={(e) => setForm({ ...form, hitl_enabled: e.target.checked })} />
          HITL activé
        </label>
        <LoadingButton loading={loading}>Générer Review</LoadingButton>
      </form>
      {error ? <ErrorMessage message={error} /> : null}
      {result ? <ResultPanel title="Résultat Review" data={result} /> : null}
    </div>
  )
}
