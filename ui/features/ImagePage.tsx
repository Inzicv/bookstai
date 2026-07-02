'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  approveHitlStep,
  editHitlStep,
  generateImageBackgroundPrompts,
  generateImageBatch,
  generateImageCharacterPrompts,
  generateImageStoryboard,
  getHitlSession,
  listBooks,
  listImageStyles,
  rejectHitlStep,
  type BookListItem,
  type ImageStyleItem,
} from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'
import { ImageStoryboardSceneCard } from '@/components/ImageStoryboardSceneCard'

type Provider = 'mock' | 'openai'
type ImageFormat = '4:5' | '1:1' | '16:9' | '9:16'

function getFriendlyErrorMessage(code: string, message: string) {
  if (code === 'MISSING_API_KEY') return 'Clé OpenAI manquante côté backend.'
  if (code === 'OPENAI_DEPENDENCY_MISSING') return 'La dépendance OpenAI n’est pas installée côté backend.'
  if (code === 'INVALID_PROVIDER') return 'Provider invalide. Choisis mock ou openai.'
  if (code === 'STYLE_NOT_FOUND') return 'Style visuel introuvable.'
  if (code === 'PROMPTS_NOT_FULLY_APPROVED') return 'Les prompts doivent être entièrement approuvés avant le batch.'
  if (code === 'GENERATION_NOT_CONFIRMED') return 'La génération doit être confirmée avant le batch.'
  return message
}

export default function ImagePage() {
  const [styles, setStyles] = useState<ImageStyleItem[]>([])
  const [books, setBooks] = useState<BookListItem[]>([])
  const [form, setForm] = useState({
    book_slug: '',
    lyrics: '',
    visual_style_id: '',
    format: '4:5' as ImageFormat,
    brief: 'Créer des visuels utilisables pour illustrer la chanson.',
    provider: 'mock' as Provider,
    model: null as string | null,
    temperature: '0.7',
    hitl_enabled: true,
  })
  const [loading, setLoading] = useState(false)
  const [stage, setStage] = useState<any>(null)
  const [characterStage, setCharacterStage] = useState<any>(null)
  const [backgroundStage, setBackgroundStage] = useState<any>(null)
  const [batchStage, setBatchStage] = useState<any>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listBooks().then((response) => response.ok && setBooks(response.books))
    listImageStyles().then((response) => response.ok && setStyles(response.styles))
  }, [])

  const currentStyle = useMemo(() => styles.find((style) => style.id === form.visual_style_id) ?? null, [form.visual_style_id, styles])
  const workflow = stage?.result ?? stage
  const storyboardScenes = workflow?.storyboard?.scenes ?? stage?.storyboard?.scenes ?? []
  const characterPrompts = characterStage?.character_prompts ?? []
  const backgroundPrompts = backgroundStage?.background_prompts ?? []
  const allStoryboardScenesApproved =
    storyboardScenes.length > 0 && storyboardScenes.every((scene: any) => scene.status === 'approved')
  const allCharacterPromptsApproved =
    characterPrompts.length > 0 && characterPrompts.every((prompt: any) => prompt.status === 'approved')
  const allBackgroundPromptsApproved =
    backgroundPrompts.length > 0 && backgroundPrompts.every((prompt: any) => prompt.status === 'approved')

  async function refreshHitlSession(itemSlug: string) {
    const session = await getHitlSession('visual', itemSlug)
    if (session.ok) {
      const steps = session.session.steps ?? []
      setStage((current: any) => (current ? { ...current, hitl: session.session } : current))
      setCharacterStage((current: any) => (current ? { ...current, hitl: session.session, character_prompts: steps.map((step) => step.content) } : current))
      setBackgroundStage((current: any) => (current ? { ...current, hitl: session.session, background_prompts: steps.map((step) => step.content) } : current))
    }
  }

  async function updateScene(stepId: string, action: 'approve' | 'reject' | 'edit', payload: any, comment?: string) {
    if (!stage?.item_slug) return
    const body = { type: 'visual', book_slug: stage.item_slug, step_id: stepId, comment, ...(action === 'edit' ? { edited_content: payload } : {}) }
    const response =
      action === 'approve' ? await approveHitlStep(body) : action === 'reject' ? await rejectHitlStep(body) : await editHitlStep(body)
    if (!response.ok) {
      setError('HITL_UPDATE_FAILED')
      return
    }
    await refreshHitlSession(stage.item_slug)
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold text-slate-100">Image</h1>
        <p className="max-w-3xl text-sm text-slate-400">
          Workflow storyboard puis prompts, basé sur la fiche de lecture et les paroles validées.
        </p>
      </div>

      <form
        className="panel grid gap-4 rounded-3xl p-6"
        onSubmit={async (event) => {
          event.preventDefault()
          setLoading(true)
          setError(null)
          const response = await generateImageStoryboard({
            book_slug: form.book_slug,
            lyrics: form.lyrics,
            visual_style_id: form.visual_style_id,
            format: form.format,
            brief: form.brief,
            provider: form.provider,
            model: form.provider === 'openai' ? form.model : null,
            temperature: Number(form.temperature),
            hitl_enabled: form.hitl_enabled,
            export_formats: [],
          })
          setLoading(false)
          if (!response.ok) return setError(getFriendlyErrorMessage(response.error.code, response.error.message))
          setStage(response)
          setCharacterStage(null)
          setBackgroundStage(null)
          setBatchStage(null)
        }}
      >
        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Livre">
            <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.book_slug} onChange={(e) => setForm({ ...form, book_slug: e.target.value })}>
              <option value="">Choisir un livre</option>
              {books.map((book) => <option key={book.slug} value={book.slug}>{book.title} ({book.slug})</option>)}
            </select>
          </FormField>
          <FormField label="Paroles de chanson">
            <textarea className="min-h-40 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.lyrics} onChange={(e) => setForm({ ...form, lyrics: e.target.value })} />
          </FormField>
        </div>

        <div className="grid gap-4 md:grid-cols-2">
          <FormField label="Style visuel">
            <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.visual_style_id} onChange={(e) => setForm({ ...form, visual_style_id: e.target.value })}>
              <option value="">Choisir un style</option>
              {styles.map((style) => <option key={style.id} value={style.id}>{style.name} ({style.id})</option>)}
            </select>
          </FormField>
          <FormField label="Format cible">
            <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.format} onChange={(e) => setForm({ ...form, format: e.target.value as ImageFormat })}>
              <option value="4:5">4:5</option><option value="1:1">1:1</option><option value="9:16">9:16</option><option value="16:9">16:9</option>
            </select>
          </FormField>
        </div>

        <FormField label="Brief complémentaire">
          <textarea className="min-h-24 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={form.brief} onChange={(e) => setForm({ ...form, brief: e.target.value })} />
        </FormField>

        <LoadingButton loading={loading}>Générer le storyboard</LoadingButton>
      </form>

      {error ? <ErrorMessage message={error} /> : null}

      {currentStyle ? (
        <section className="panel rounded-3xl p-6">
          <h2 className="text-lg font-semibold text-slate-50">Instructions du style sélectionné</h2>
          <pre className="mt-4 whitespace-pre-wrap rounded-2xl border border-slate-800 bg-slate-950/80 p-4 text-sm text-slate-100">{currentStyle.instructions}</pre>
        </section>
      ) : null}

      {workflow?.storyboard?.scenes ? (
        <section className="space-y-4">
          <h2 className="text-lg font-semibold text-slate-50">Storyboard</h2>
          <div className="grid gap-4">
            {workflow.storyboard.scenes.map((scene: any) => (
              <ImageStoryboardSceneCard
                key={scene.scene_id}
                scene={scene}
                onApprove={(comment: string) => updateScene(scene.scene_id, 'approve', null, comment)}
                onReject={(comment: string) => updateScene(scene.scene_id, 'reject', null, comment)}
                onEdit={(edited: any, comment: string) => updateScene(scene.scene_id, 'edit', edited, comment)}
              />
            ))}
          </div>
        </section>
      ) : null}

      {workflow?.item_slug ? (
        <section className="space-y-4">
          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Prompts personnages</h2>
            {allStoryboardScenesApproved ? (
              <button
                className="mt-3 rounded-xl bg-sky-500 px-4 py-2 text-slate-950"
                onClick={async () => {
                  const response = await generateImageCharacterPrompts({
                    item_slug: workflow.item_slug,
                    book_slug: form.book_slug,
                    visual_style_id: form.visual_style_id,
                    storyboard: workflow.storyboard,
                  })
                  if (response.ok) setCharacterStage(response)
                }}
              >
                Générer les prompts personnages
              </button>
            ) : (
              <p className="mt-2 text-sm text-slate-400">Valide d’abord toutes les scènes du storyboard.</p>
            )}
            {characterPrompts.map((prompt: any) => <pre key={prompt.prompt_id} className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm">{JSON.stringify(prompt, null, 2)}</pre>)}
          </div>

          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Prompts décors</h2>
            {allCharacterPromptsApproved ? (
              <button
                className="mt-3 rounded-xl bg-sky-500 px-4 py-2 text-slate-950"
                onClick={async () => {
                  const response = await generateImageBackgroundPrompts({
                    item_slug: workflow.item_slug,
                    book_slug: form.book_slug,
                    visual_style_id: form.visual_style_id,
                    storyboard: workflow.storyboard,
                    character_prompts: characterPrompts,
                  })
                  if (response.ok) setBackgroundStage(response)
                }}
              >
                Générer les prompts décors
              </button>
            ) : (
              <p className="mt-2 text-sm text-slate-400">Valide d’abord tous les prompts personnages.</p>
            )}
            {backgroundPrompts.map((prompt: any) => <pre key={prompt.prompt_id} className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm">{JSON.stringify(prompt, null, 2)}</pre>)}
          </div>

          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Génération batch</h2>
            {allCharacterPromptsApproved && allBackgroundPromptsApproved ? (
              <button
                className="mt-3 rounded-xl bg-emerald-500 px-4 py-2 text-slate-950"
                onClick={async () => {
                  const response = await generateImageBatch({
                    item_slug: workflow.item_slug,
                    storyboard: workflow.storyboard,
                    character_prompts: characterPrompts,
                    background_prompts: backgroundPrompts,
                    backend: 'mock',
                    confirm_generation: true,
                  })
                  if (response.ok) setBatchStage(response)
                }}
              >
                Générer les images en lot
              </button>
            ) : (
              <p className="mt-2 text-sm text-slate-400">Tous les prompts doivent être approuvés.</p>
            )}
            {batchStage?.images ? <pre className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm">{JSON.stringify(batchStage.images, null, 2)}</pre> : null}
          </div>
        </section>
      ) : null}
    </div>
  )
}
