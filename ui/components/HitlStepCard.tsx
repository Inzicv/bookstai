'use client'

import { useState } from 'react'
import { JsonBlock } from './JsonBlock'

function formatValue(value: unknown) {
  if (value === undefined) return '—'
  if (typeof value === 'string') return value || '—'
  return JSON.stringify(value, null, 2)
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
  const [editedContent, setEditedContent] = useState(
    JSON.stringify(step.validated_content ?? step.content ?? '', null, 2),
  )
  const [comment, setComment] = useState(step.comment ?? '')

  return (
    <div className="panel space-y-4 rounded-3xl p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold">{step.name}</h3>
          <p className="text-sm text-zinc-600">Status: {step.status}</p>
        </div>
        <div className="flex flex-wrap gap-2">
          <button className="rounded-full bg-emerald-600 px-4 py-2 text-sm text-white" onClick={() => onApprove(comment)}>
            Approuver
          </button>
          <button className="rounded-full bg-rose-600 px-4 py-2 text-sm text-white" onClick={() => onReject(comment)}>
            Rejeter
          </button>
          <button className="rounded-full bg-zinc-900 px-4 py-2 text-sm text-white" onClick={() => onEdit(editedContent, comment)}>
            Modifier
          </button>
        </div>
      </div>

      <div className="grid gap-3 text-sm md:grid-cols-2">
        {[
          ['content', step.content],
          ['edited_content', step.edited_content],
          ['validated_content', step.validated_content],
          ['comment', step.comment],
        ].map(([label, value]) => (
          <div key={label} className="rounded-2xl border border-zinc-200 bg-white/60 p-3">
            <div className="text-xs uppercase tracking-[0.18em] text-zinc-500">{label}</div>
            <pre className="mt-2 overflow-auto whitespace-pre-wrap break-words text-xs text-zinc-800">
              {formatValue(value)}
            </pre>
          </div>
        ))}
      </div>

      <label className="grid gap-2 text-sm">
        <span>comment</span>
        <input className="rounded-xl border border-zinc-200 px-3 py-2" value={comment} onChange={(e) => setComment(e.target.value)} />
      </label>
      <label className="grid gap-2 text-sm">
        <span>edited_content</span>
        <textarea className="min-h-28 rounded-xl border border-zinc-200 px-3 py-2 font-mono text-xs" value={editedContent} onChange={(e) => setEditedContent(e.target.value)} />
      </label>

      <div className="grid gap-2 text-sm">
        <span>metadata</span>
        <JsonBlock value={step.metadata ?? {}} />
      </div>
    </div>
  )
}
