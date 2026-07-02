'use client'

import { useState } from 'react'
import { runSocial } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'
import { BookSelect } from '@/components/BookSelect'

export default function SocialPage() {
  const [form, setForm] = useState({ book_slug: 'alchemised', source_type: 'review', source_content: '', provider: 'mock', model: null as string | null })
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold text-slate-100">Social</h1>
      <form className="panel grid gap-4 rounded-3xl p-6" onSubmit={async (e) => { e.preventDefault(); setLoading(true); setError(null); const r = await runSocial(form as any); setLoading(false); if (!r.ok) return setError(r.error.message); setResult(r); }}>
        <BookSelect value={form.book_slug} onChange={(book_slug) => setForm({ ...form, book_slug })} />
        <FormField label="Type de contenu source">
          <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.source_type} onChange={(e) => setForm({ ...form, source_type: e.target.value })}>
            <option value="review">Review</option>
            <option value="song">Song</option>
            <option value="free_text">Texte libre</option>
          </select>
        </FormField>
        <FormField label="Texte source">
          <textarea className="min-h-32 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.source_content} onChange={(e) => setForm({ ...form, source_content: e.target.value })} />
        </FormField>
        <LoadingButton loading={loading}>Générer Social</LoadingButton>
      </form>
      {error ? <ErrorMessage message={error} /> : null}
      {result ? <section className="panel space-y-4 rounded-3xl p-6"><div><h2 className="text-lg font-semibold text-slate-50">Légende Instagram</h2><p className="whitespace-pre-wrap text-slate-200">{result.result.instagram_caption}</p></div><div><h2 className="text-lg font-semibold text-slate-50">Légende TikTok</h2><p className="whitespace-pre-wrap text-slate-200">{result.result.tiktok_caption}</p></div></section> : null}
    </div>
  )
}
