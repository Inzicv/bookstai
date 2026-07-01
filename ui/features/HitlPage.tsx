'use client'

import { useState } from 'react'
import { approveHitlStep, editHitlStep, getHitlSession, rejectHitlStep } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { ResultPanel } from '@/components/ResultPanel'
import { HitlStepCard } from '@/components/HitlStepCard'
import { FormField } from '@/components/FormField'

export default function HitlPage() {
  const [type, setType] = useState<'review' | 'song'>('review')
  const [bookSlug, setBookSlug] = useState('alchemised')
  const [session, setSession] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  async function refresh() {
    setLoading(true)
    setError(null)
    const response = await getHitlSession(type, bookSlug)
    setLoading(false)
    if (!response.ok) {
      setError(response.error.message)
      setSession(null)
      return
    }
    setSession(response)
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">HITL</h1>
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
          <LoadingButton loading={loading} onClick={refresh}>Charger la session</LoadingButton>
        </div>
      </div>
      {error ? <ErrorMessage message={error} /> : null}
      {session?.session?.steps ? (
        <div className="space-y-4">
          {session.session.steps.map((step: any) => (
            <HitlStepCard
              key={step.name}
              step={step}
              onApprove={async (comment) => {
                await approveHitlStep({ type, book_slug: bookSlug, step_id: step.name, comment })
                await refresh()
              }}
              onReject={async (comment) => {
                await rejectHitlStep({ type, book_slug: bookSlug, step_id: step.name, comment })
                await refresh()
              }}
              onEdit={async (edited_content, comment) => {
                await editHitlStep({ type, book_slug: bookSlug, step_id: step.name, edited_content, comment })
                await refresh()
              }}
            />
          ))}
          <ResultPanel title="Session HITL" data={session} />
        </div>
      ) : null}
    </div>
  )
}

