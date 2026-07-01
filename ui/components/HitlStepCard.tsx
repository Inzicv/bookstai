'use client'

import { useMemo, useState } from 'react'
import { JsonBlock } from './JsonBlock'

function normalizeContent(value: unknown): string {
  if (value === undefined || value === null) return '—'
  if (typeof value === 'string') return value.trim() || '—'
  if (typeof value !== 'object') return String(value)

  const record = value as Record<string, unknown>
  const response = record.response
  if (typeof response === 'string' && response.trim()) return response

  if (Array.isArray(value)) return JSON.stringify(value, null, 2)

  return JSON.stringify(value, null, 2)
}

function pickInitialEditableContent(step: any): string {
  const preferred = step.edited_content ?? step.validated_content ?? step.content
  if (typeof preferred === 'string') return preferred
  return normalizeContent(preferred)
}

function formatSummary(value: unknown): string {
  if (value === undefined || value === null) return '—'
  if (typeof value === 'string') return value || '—'
  return normalizeContent(value)
}

export function HitlStepCard({
  step,
  onApprove,
  onReject,
  onEdit,
}: {
  step: any
  onApprove: (comment?: string) => Promise<void>
  onReject: (comment?: string) => Promise<void>
  onEdit: (editedContent: string, comment?: string) => Promise<void>
}) {
  const [editedContent, setEditedContent] = useState(pickInitialEditableContent(step))
  const [comment, setComment] = useState(step.comment ?? '')
  const [showDebug, setShowDebug] = useState(false)

  const contentPreview = useMemo(
    () => formatSummary(step.edited_content ?? step.content),
    [step.edited_content, step.content],
  )

  return (
    <div className="panel space-y-4 rounded-3xl p-6">
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="space-y-1">
          <h3 className="text-lg font-semibold text-slate-100">{step.name}</h3>
          <p className="text-sm text-slate-400">Statut: {step.status}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button
            className="rounded-full bg-emerald-500 px-4 py-2 text-sm font-medium text-slate-950 transition hover:bg-emerald-400"
            onClick={() => onApprove(comment)}
          >
            Approuver
          </button>
          <button
            className="rounded-full bg-amber-500 px-4 py-2 text-sm font-medium text-slate-950 transition hover:bg-amber-400"
            onClick={() => onEdit(editedContent, comment)}
          >
            Modifier
          </button>
          <button
            className="rounded-full bg-rose-500 px-4 py-2 text-sm font-medium text-white transition hover:bg-rose-400"
            onClick={() => onReject(comment)}
          >
            Rejeter
          </button>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-[1.2fr_0.8fr]">
        <div className="space-y-2 rounded-2xl border border-slate-700 bg-slate-900/80 p-4">
          <div className="text-xs uppercase tracking-[0.18em] text-slate-400">Contenu principal</div>
          <pre className="whitespace-pre-wrap break-words text-sm leading-6 text-slate-100">
            {contentPreview}
          </pre>
        </div>

        <div className="space-y-3 rounded-2xl border border-slate-700 bg-slate-900/80 p-4">
          <label className="grid gap-2 text-sm text-slate-300">
            <span className="text-xs uppercase tracking-[0.18em] text-slate-400">Commentaire</span>
            <input
              className="rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Commentaire optionnel"
            />
          </label>
          <label className="grid gap-2 text-sm text-slate-300">
            <span className="text-xs uppercase tracking-[0.18em] text-slate-400">Modification</span>
            <textarea
              className="min-h-32 rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs text-slate-100 placeholder:text-slate-500"
              value={editedContent}
              onChange={(e) => setEditedContent(e.target.value)}
              placeholder="Contenu à modifier"
            />
          </label>
        </div>
      </div>

      <div className="border-t border-slate-800 pt-4">
        <button
          type="button"
          className="text-sm font-medium text-slate-300 transition hover:text-slate-100"
          onClick={() => setShowDebug((value) => !value)}
        >
          {showDebug ? 'Masquer le debug JSON' : 'Afficher le debug JSON'}
        </button>
        {showDebug ? (
          <div className="mt-4 grid gap-3 text-sm md:grid-cols-2">
            {[
              ['content', step.content],
              ['edited_content', step.edited_content],
              ['validated_content', step.validated_content],
              ['comment', step.comment],
              ['metadata', step.metadata ?? {}],
            ].map(([label, value]) => (
              <div key={label} className="rounded-2xl border border-slate-700 bg-slate-950/80 p-3">
                <div className="text-xs uppercase tracking-[0.18em] text-slate-400">{label}</div>
                {label === 'metadata' ? (
                  <div className="mt-2">
                    <JsonBlock value={value} />
                  </div>
                ) : (
                  <pre className="mt-2 whitespace-pre-wrap break-words text-xs leading-6 text-slate-200">
                    {formatSummary(value)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        ) : null}
      </div>
    </div>
  )
}
