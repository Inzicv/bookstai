'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  approveHitlStep,
  editHitlStep,
  getHitlSession,
  rejectHitlStep,
  runReview,
} from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'
import { BookSelect } from '@/components/BookSelect'
import { HitlStepCard } from '@/components/HitlStepCard'

type Provider = 'mock' | 'openai'
type OpenAIModel = 'gpt-5.5' | 'gpt-5.4' | 'gpt-5.4-mini' | 'gpt-5.4-nano'

const OPENAI_MODEL_OPTIONS: Array<{ value: OpenAIModel; label: string }> = [
  { value: 'gpt-5.5', label: 'GPT-5.5 â€” meilleur choix qualitÃ© / raisonnement' },
  { value: 'gpt-5.4', label: 'GPT-5.4 â€” bon Ã©quilibre qualitÃ© / coÃ»t' },
  { value: 'gpt-5.4-mini', label: 'GPT-5.4 mini â€” plus rapide et moins cher' },
  { value: 'gpt-5.4-nano', label: 'GPT-5.4 nano â€” Ã©conomique pour tests simples' },
]

function getFriendlyErrorMessage(code: string, message: string) {
  if (code === 'MISSING_API_KEY') {
    return 'ClÃ© OpenAI manquante cÃ´tÃ© backend. Configure OPENAI_API_KEY puis relance lâ€™API.'
  }
  if (code === 'OPENAI_DEPENDENCY_MISSING') {
    return 'La dÃ©pendance OpenAI nâ€™est pas installÃ©e cÃ´tÃ© backend. Installe lâ€™extra openai du projet.'
  }
  if (code === 'INVALID_PROVIDER') {
    return 'Provider invalide. Choisis mock ou openai.'
  }
  return message
}

export default function ReviewPage() {
  const [form, setForm] = useState({
    book_slug: 'alchemised',
    user_opinion: '',
    provider: 'mock' as Provider,
    model: null as OpenAIModel | null,
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
  const hitlSteps = workflow?.hitl?.steps ?? []
  const pitchStep = useMemo(
    () =>
      hitlSteps.find((step: any) => step.name === 'pitch_options') ??
      (workflow?.pitch_options
        ? { name: 'pitch_options', status: 'pending', content: workflow.pitch_options }
        : null),
    [hitlSteps, workflow?.pitch_options],
  )
  const reviewStep = useMemo(
    () =>
      hitlSteps.find((step: any) => step.name === 'review') ??
      (workflow?.review ? { name: 'review', status: 'pending', content: workflow.review } : null),
    [hitlSteps, workflow?.review],
  )

  async function refreshHitlSession() {
    if (!result?.result?.hitl) return
    const session = await getHitlSession('review', form.book_slug)
    if (session.ok) {
      setResult((current: any) =>
        current
          ? {
              ...current,
              result: {
                ...current.result,
                hitl: session.session,
              },
            }
          : current,
      )
    }
  }

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
            model: form.provider === 'openai' ? form.model : null,
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
        <FormField label="Avis personnel">
          <textarea
            className="min-h-32 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
            value={form.user_opinion}
            onChange={(e) => setForm({ ...form, user_opinion: e.target.value })}
          />
        </FormField>
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Provider texte">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.provider}
              onChange={(e) => setForm({ ...form, provider: e.target.value as Provider })}
            >
              <option value="mock">Mock â€” test local sans coÃ»t</option>
              <option value="openai">OpenAI â€” gÃ©nÃ©ration texte rÃ©elle</option>
            </select>
            <p className="text-xs text-slate-400">
              La clÃ© OpenAI est lue cÃ´tÃ© backend depuis{' '}
              <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-100">
                OPENAI_API_KEY
              </code>
              . Elle ne doit jamais Ãªtre saisie ici.
            </p>
          </FormField>
        </div>
        {form.provider === 'openai' ? (
          <div className="grid gap-4 md:grid-cols-2">
            <FormField label="ModÃ¨le OpenAI">
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
                Pour commencer, utilise GPT-5.4 mini : bon compromis entre qualitÃ©, vitesse et coÃ»t.
              </p>
            </FormField>
            <FormField label="TempÃ©rature">
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
            Le provider mock nâ€™utilise pas de vrai modÃ¨le.
          </div>
        )}
        <label className="flex items-center gap-2 text-sm text-slate-300">
          <input
            type="checkbox"
            checked={form.hitl_enabled}
            onChange={(e) => setForm({ ...form, hitl_enabled: e.target.checked })}
          />
          HITL activÃ©
        </label>
        <LoadingButton loading={loading}>GÃ©nÃ©rer Review</LoadingButton>
      </form>

      {error ? <ErrorMessage message={error} /> : null}

      {result && pitchStep && reviewStep ? (
        <section className="space-y-6">
          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Validation</h2>
            <p className="mt-2 text-sm text-slate-400">
              Valide, modifie ou rejette directement les deux sorties principales.
            </p>
          </div>
          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Pitchs proposÃ©s</h2>
            <div className="mt-4">
              <HitlStepCard
                step={pitchStep}
                onApprove={async (comment) => {
                  await approveHitlStep({
                    type: 'review',
                    book_slug: form.book_slug,
                    step_id: pitchStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onReject={async (comment) => {
                  await rejectHitlStep({
                    type: 'review',
                    book_slug: form.book_slug,
                    step_id: pitchStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onEdit={async (editedContent, comment) => {
                  await editHitlStep({
                    type: 'review',
                    book_slug: form.book_slug,
                    step_id: pitchStep.name,
                    edited_content: editedContent,
                    comment,
                  })
                  await refreshHitlSession()
                }}
              />
            </div>
          </div>

          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Avis reformulÃ©</h2>
            <div className="mt-4">
              <HitlStepCard
                step={reviewStep}
                onApprove={async (comment) => {
                  await approveHitlStep({
                    type: 'review',
                    book_slug: form.book_slug,
                    step_id: reviewStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onReject={async (comment) => {
                  await rejectHitlStep({
                    type: 'review',
                    book_slug: form.book_slug,
                    step_id: reviewStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onEdit={async (editedContent, comment) => {
                  await editHitlStep({
                    type: 'review',
                    book_slug: form.book_slug,
                    step_id: reviewStep.name,
                    edited_content: editedContent,
                    comment,
                  })
                  await refreshHitlSession()
                }}
              />
            </div>
          </div>
        </section>
      ) : null}
    </div>
  )
}
