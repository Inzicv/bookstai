'use client'

import { useState } from 'react'
import { applyLearning, draftLearning, extractLearning } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { ResultPanel } from '@/components/ResultPanel'
import { FormField } from '@/components/FormField'

export default function LearningPage() {
  const [type, setType] = useState<'review' | 'song'>('review')
  const [bookSlug, setBookSlug] = useState('alchemised')
  const [result, setResult] = useState<any>(null)
  const [draft, setDraft] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function loadExtraction() {
    setLoading(true)
    setError(null)
    const response = await extractLearning({ type, book_slug: bookSlug })
    setLoading(false)
    if (!response.ok) {
      setError(response.error.message)
      return
    }
    setResult(response)
  }

  async function createDraft() {
    setLoading(true)
    setError(null)
    const response = await draftLearning({ type, book_slug: bookSlug })
    setLoading(false)
    if (!response.ok) {
      setError(response.error.message)
      return
    }
    setDraft(response)
  }

  async function applyDraft() {
    if (!draft?.draft_path) return
    if (!window.confirm('Appliquer ce draft à la mémoire locale ?')) return
    setLoading(true)
    setError(null)
    const response = await applyLearning({ draft_path: draft.draft_path, confirm: true })
    setLoading(false)
    if (!response.ok) {
      setError(response.error.message)
      return
    }
    setResult(response)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Learning</h1>
      <div className="panel grid gap-4 rounded-3xl p-6 md:grid-cols-[1fr_1fr_auto]">
        <FormField label="type">
          <select className="w-full rounded-xl border border-zinc-200 px-3 py-2" value={type} onChange={(e) => setType(e.target.value as 'review' | 'song')}>
            <option value="review">review</option>
            <option value="song">song</option>
          </select>
        </FormField>
        <FormField label="book_slug">
          <input className="w-full rounded-xl border border-zinc-200 px-3 py-2" value={bookSlug} onChange={(e) => setBookSlug(e.target.value)} />
        </FormField>
        <div className="flex items-end">
          <LoadingButton loading={loading} onClick={loadExtraction}>Extraire les apprentissages</LoadingButton>
        </div>
      </div>
      <div className="flex flex-wrap gap-3">
        <LoadingButton loading={loading} onClick={createDraft}>Générer le draft</LoadingButton>
        <LoadingButton loading={loading} onClick={applyDraft}>Appliquer à la mémoire</LoadingButton>
      </div>
      {error ? <ErrorMessage message={error} /> : null}
      {result ? <ResultPanel title="Résultat Learning" data={result} /> : null}
      {draft ? <ResultPanel title="Draft Markdown" data={{ draft_path: draft.draft_path, markdown: draft.markdown }} /> : null}
    </div>
  )
}

