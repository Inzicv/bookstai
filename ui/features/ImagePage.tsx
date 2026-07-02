'use client'

import { useEffect, useMemo, useState } from 'react'
import { approveHitlStep, editHitlStep, getHitlSession, listImageStyles, rejectHitlStep, runImage, type ImageStyleItem } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'
import { HitlStepCard } from '@/components/HitlStepCard'

type Provider = 'mock' | 'openai'
type ImageFormat = '4:5' | '1:1' | '16:9' | '9:16'
type Platform = 'instagram' | 'tiktok' | 'youtube_shorts'

function getFriendlyErrorMessage(code: string, message: string) {
  if (code === 'MISSING_API_KEY') {
    return 'Clé OpenAI manquante côté backend. Configure OPENAI_API_KEY puis relance l’API.'
  }
  if (code === 'OPENAI_DEPENDENCY_MISSING') {
    return 'La dépendance OpenAI n’est pas installée côté backend. Installe l’extra openai du projet.'
  }
  if (code === 'INVALID_PROVIDER') {
    return 'Provider invalide. Choisis mock ou openai.'
  }
  if (code === 'STYLE_NOT_FOUND') {
    return 'Style visuel introuvable. Vérifie les fichiers dans memory/visual_style/Prompts_visuels/.'
  }
  return message
}

export default function ImagePage() {
  const [styles, setStyles] = useState<ImageStyleItem[]>([])
  const [loadingStyles, setLoadingStyles] = useState(false)
  const [styleError, setStyleError] = useState<string | null>(null)
  const [form, setForm] = useState({
    lyrics: '',
    visual_style_id: '',
    platform: 'instagram' as Platform,
    format: '4:5' as ImageFormat,
    brief: 'Créer des visuels utilisables pour illustrer la chanson.',
    provider: 'mock' as Provider,
    model: null as string | null,
    temperature: '0.7',
    hitl_enabled: true,
    export_markdown: true,
    export_json: true,
  })
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function loadStyles() {
      setLoadingStyles(true)
      setStyleError(null)
      const response = await listImageStyles()
      setLoadingStyles(false)
      if (!response.ok) {
        setStyleError(getFriendlyErrorMessage(response.error.code, response.error.message))
        return
      }
      setStyles(response.styles)
      setForm((current) => ({
        ...current,
        visual_style_id: current.visual_style_id || response.styles[0]?.id || '',
      }))
    }

    loadStyles()
  }, [])

  useEffect(() => {
    if (form.provider === 'openai' && !form.model) {
      setForm((current) => ({ ...current, model: 'gpt-5.4-mini' }))
    }
    if (form.provider === 'mock' && form.model !== null) {
      setForm((current) => ({ ...current, model: null }))
    }
  }, [form.model, form.provider])

  const currentStyle = useMemo(
    () => styles.find((style) => style.id === form.visual_style_id) ?? null,
    [form.visual_style_id, styles],
  )

  const workflow = result?.result
  const hitlSteps = workflow?.hitl?.steps ?? []
  const styleStep = useMemo(
    () =>
      hitlSteps.find((step: any) => step.name === 'style_selection') ??
      (workflow?.style_selection
        ? { name: 'style_selection', status: 'pending', content: workflow.style_selection }
        : null),
    [hitlSteps, workflow?.style_selection],
  )
  const storyboardStep = useMemo(
    () =>
      hitlSteps.find((step: any) => step.name === 'storyboard') ??
      (workflow?.storyboard ? { name: 'storyboard', status: 'pending', content: workflow.storyboard } : null),
    [hitlSteps, workflow?.storyboard],
  )
  const promptsStep = useMemo(
    () =>
      hitlSteps.find((step: any) => step.name === 'prompts') ??
      (workflow?.prompts ? { name: 'prompts', status: 'pending', content: workflow.prompts } : null),
    [hitlSteps, workflow?.prompts],
  )

  async function refreshHitlSession() {
    if (!result?.result?.hitl) return
    const session = await getHitlSession('visual', form.visual_style_id)
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
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold text-slate-100">Image</h1>
        <p className="max-w-3xl text-sm text-slate-400">
          Relance la partie visuelle à partir des paroles d’une chanson déjà validée. Le style
          sélectionné vient uniquement de <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-100">memory/visual_style/Prompts_visuels</code>.
        </p>
      </div>

      <form
        className="panel grid gap-4 rounded-3xl p-6"
        onSubmit={async (event) => {
          event.preventDefault()
          setLoading(true)
          setError(null)
          setResult(null)
          const response = await runImage({
            lyrics: form.lyrics,
            visual_style_id: form.visual_style_id,
            platform: form.platform,
            format: form.format,
            brief: form.brief,
            provider: form.provider,
            model: form.provider === 'openai' ? form.model : null,
            temperature: Number(form.temperature),
            hitl_enabled: form.hitl_enabled,
            export_formats: [
              ...(form.export_markdown ? ['markdown'] : []),
              ...(form.export_json ? ['json'] : []),
            ],
          })
          setLoading(false)
          if (!response.ok) {
            setError(getFriendlyErrorMessage(response.error.code, response.error.message))
            return
          }
          setResult(response)
        }}
      >
        <FormField label="Paroles de chanson">
          <textarea
            className="min-h-40 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
            value={form.lyrics}
            onChange={(e) => setForm({ ...form, lyrics: e.target.value })}
            placeholder="Colle ici les paroles finales de la chanson..."
          />
        </FormField>

        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Style visuel">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.visual_style_id}
              onChange={(e) => setForm({ ...form, visual_style_id: e.target.value })}
              disabled={loadingStyles}
            >
              <option value="">Choisir un style</option>
              {styles.map((style) => (
                <option key={style.id} value={style.id}>
                  {style.name} ({style.id})
                </option>
              ))}
            </select>
            <p className="text-xs text-slate-400">
              {loadingStyles
                ? 'Chargement des styles visuels...'
                : 'La liste est lue automatiquement depuis les fichiers Markdown du dossier visual_style.'}
            </p>
          </FormField>

          <FormField label="Format cible">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.format}
              onChange={(e) => setForm({ ...form, format: e.target.value as ImageFormat })}
            >
              <option value="4:5">4:5</option>
              <option value="1:1">1:1</option>
              <option value="9:16">9:16</option>
              <option value="16:9">16:9</option>
            </select>
          </FormField>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Brief complémentaire">
            <textarea
              className="min-h-24 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
              value={form.brief}
              onChange={(e) => setForm({ ...form, brief: e.target.value })}
            />
          </FormField>
          <FormField label="Plateforme">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.platform}
              onChange={(e) => setForm({ ...form, platform: e.target.value as Platform })}
            >
              <option value="instagram">Instagram</option>
              <option value="tiktok">TikTok</option>
              <option value="youtube_shorts">YouTube Shorts</option>
            </select>
          </FormField>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Provider texte">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.provider}
              onChange={(e) => setForm({ ...form, provider: e.target.value as Provider })}
            >
              <option value="mock">Mock — test local sans coût</option>
              <option value="openai">OpenAI — génération texte réelle</option>
            </select>
            <p className="text-xs text-slate-400">
              La clé OpenAI est lue côté backend depuis{' '}
              <code className="rounded bg-slate-800 px-1.5 py-0.5 text-slate-100">
                OPENAI_API_KEY
              </code>
              . Elle ne doit jamais être saisie ici.
            </p>
          </FormField>

          <FormField label="Température">
            <input
              type="number"
              step="0.1"
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100 placeholder:text-slate-500"
              value={form.temperature}
              onChange={(e) => setForm({ ...form, temperature: e.target.value })}
            />
          </FormField>
        </div>

        {form.provider === 'openai' ? (
          <FormField label="Modèle OpenAI">
            <select
              className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
              value={form.model ?? 'gpt-5.4-mini'}
              onChange={(e) => setForm({ ...form, model: e.target.value })}
            >
              <option value="gpt-5.4-mini">GPT-5.4 mini — équilibre qualité / coût</option>
              <option value="gpt-5.4">GPT-5.4 — plus de raisonnement</option>
              <option value="gpt-5.5">GPT-5.5 — meilleure qualité</option>
              <option value="gpt-5.4-nano">GPT-5.4 nano — économique</option>
            </select>
          </FormField>
        ) : (
          <div className="rounded-2xl border border-slate-800 bg-slate-950/60 px-4 py-3 text-sm text-slate-300">
            Le provider mock n’utilise pas de vrai modèle.
          </div>
        )}

        <div className="flex flex-wrap gap-4">
          <label className="flex items-center gap-2 text-sm text-slate-300">
            <input
              type="checkbox"
              checked={form.hitl_enabled}
              onChange={(e) => setForm({ ...form, hitl_enabled: e.target.checked })}
            />
            HITL activé
          </label>
          <label className="flex items-center gap-2 text-sm text-slate-300">
            <input
              type="checkbox"
              checked={form.export_markdown}
              onChange={(e) => setForm({ ...form, export_markdown: e.target.checked })}
            />
            Export Markdown
          </label>
          <label className="flex items-center gap-2 text-sm text-slate-300">
            <input
              type="checkbox"
              checked={form.export_json}
              onChange={(e) => setForm({ ...form, export_json: e.target.checked })}
            />
            Export JSON
          </label>
        </div>

        <LoadingButton loading={loading}>Générer Image</LoadingButton>
      </form>

      {styleError ? <ErrorMessage message={styleError} /> : null}
      {error ? <ErrorMessage message={error} /> : null}

      {currentStyle ? (
        <section className="panel rounded-3xl p-6">
          <h2 className="text-lg font-semibold text-slate-50">Instructions du style sélectionné</h2>
          <p className="mt-2 text-sm text-slate-400">
            {currentStyle.name} · {currentStyle.source_path}
          </p>
          <pre className="mt-4 max-h-96 overflow-auto whitespace-pre-wrap break-words rounded-2xl border border-slate-800 bg-slate-950/80 p-4 text-sm leading-6 text-slate-100">
            {currentStyle.instructions}
          </pre>
        </section>
      ) : null}

      {result && styleStep && storyboardStep && promptsStep ? (
        <section className="space-y-6">
          {result.export_paths ? (
            <div className="panel rounded-3xl p-6">
              <h2 className="text-lg font-semibold text-slate-50">Exports</h2>
              <ul className="mt-3 space-y-1 text-sm text-slate-300">
                {Object.entries(result.export_paths as Record<string, string>).map(([format, path]) => (
                  <li key={format}>
                    {format.toUpperCase()} · {path}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}

          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Style visuel validé</h2>
            <div className="mt-4">
              <HitlStepCard
                step={styleStep}
                onApprove={async (comment) => {
                  await approveHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: styleStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onReject={async (comment) => {
                  await rejectHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: styleStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onEdit={async (editedContent, comment) => {
                  await editHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: styleStep.name,
                    edited_content: editedContent,
                    comment,
                  })
                  await refreshHitlSession()
                }}
              />
            </div>
          </div>

          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Storyboard</h2>
            <div className="mt-4">
              <HitlStepCard
                step={storyboardStep}
                onApprove={async (comment) => {
                  await approveHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: storyboardStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onReject={async (comment) => {
                  await rejectHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: storyboardStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onEdit={async (editedContent, comment) => {
                  await editHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: storyboardStep.name,
                    edited_content: editedContent,
                    comment,
                  })
                  await refreshHitlSession()
                }}
              />
            </div>
          </div>

          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Prompts finaux</h2>
            <div className="mt-4">
              <HitlStepCard
                step={promptsStep}
                onApprove={async (comment) => {
                  await approveHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: promptsStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onReject={async (comment) => {
                  await rejectHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: promptsStep.name,
                    comment,
                  })
                  await refreshHitlSession()
                }}
                onEdit={async (editedContent, comment) => {
                  await editHitlStep({
                    type: 'visual',
                    book_slug: form.visual_style_id,
                    step_id: promptsStep.name,
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
