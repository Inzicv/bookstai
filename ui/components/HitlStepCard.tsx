'use client'

import { useState } from 'react'
import { JsonBlock } from './JsonBlock'

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
  const [editedContent, setEditedContent] = useState(JSON.stringify(step.validated_content ?? step.content, null, 2))
  const [comment, setComment] = useState(step.comment ?? '')
  return (
    <div className="panel space-y-4 rounded-3xl p-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold">{step.name}</h3>
          <p className="text-sm text-zinc-600">{step.status}</p>
        </div>
        <div className="flex gap-2">
          <button className="rounded-full bg-emerald-600 px-4 py-2 text-sm text-white" onClick={() => onApprove(comment)}>Approuver</button>
          <button className="rounded-full bg-rose-600 px-4 py-2 text-sm text-white" onClick={() => onReject(comment)}>Rejeter</button>
          <button className="rounded-full bg-zinc-900 px-4 py-2 text-sm text-white" onClick={() => onEdit(editedContent, comment)}>Modifier</button>
        </div>
      </div>
      <label className="grid gap-2 text-sm">
        <span>comment</span>
        <input className="rounded-xl border border-zinc-200 px-3 py-2" value={comment} onChange={(e) => setComment(e.target.value)} />
      </label>
      <label className="grid gap-2 text-sm">
        <span>edited_content</span>
        <textarea className="min-h-28 rounded-xl border border-zinc-200 px-3 py-2 font-mono text-xs" value={editedContent} onChange={(e) => setEditedContent(e.target.value)} />
      </label>
      <JsonBlock value={step} />
    </div>
  )
}

