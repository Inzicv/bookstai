'use client'

import { useEffect, useMemo, useState } from 'react'
import {
  approveImageStoryboard,
  generateImageBackgroundPrompts,
  generateImageBatch,
  generateImageCharacterPrompts,
  generateImageStoryboard,
  listBooks,
  listImageStyles,
  type BookListItem,
  type ImageStyleItem,
} from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'

type Provider = 'mock' | 'openai'
type ImageFormat = '4:5' | '1:1' | '16:9' | '9:16'
type SceneStatus = 'pending' | 'approved' | 'rejected' | 'edited'

type Scene = {
  scene_id: string
  scene_number: number
  song_part: string
  lyrics_excerpt: string
  visual_intention: string
  characters: string[]
  background: string
  key_props: string[]
  camera: string
  movement: string
  transition: string
  style_notes: string
  status: SceneStatus
  comment?: string
}

function getFriendlyErrorMessage(code: string, message: string) {
  if (code === 'STORYBOARD_EMPTY') return 'Le storyboard doit contenir au moins une scène.'
  if (code === 'STORYBOARD_NOT_FULLY_APPROVED') return 'Toutes les scènes doivent être validées ou modifiées.'
  if (code === 'STORYBOARD_SAVE_FAILED') return 'Impossible de sauvegarder le storyboard validé.'
  return message
}

function ImageStoryboardSceneCard({
  scene,
  onApprove,
  onReject,
  onEdit,
}: {
  scene: Scene
  onApprove: () => void
  onReject: (comment: string) => void
  onEdit: (edited: string, comment: string) => void
}) {
  const [comment, setComment] = useState(scene.comment ?? '')
  const [edited, setEdited] = useState(JSON.stringify(scene, null, 2))

  return (
    <div className="panel rounded-3xl p-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-lg font-semibold text-slate-100">
            Scène {scene.scene_number} · {scene.scene_id}
          </h3>
          <p className="text-sm text-slate-400">Statut: {scene.status}</p>
        </div>
        <div className="flex gap-2">
          <button type="button" className="rounded-full bg-emerald-500 px-4 py-2 text-sm text-slate-950" onClick={onApprove}>
            Valider
          </button>
          <button type="button" className="rounded-full bg-amber-500 px-4 py-2 text-sm text-slate-950" onClick={() => onEdit(edited, comment)}>
            Modifier
          </button>
          <button type="button" className="rounded-full bg-rose-500 px-4 py-2 text-sm text-white" onClick={() => onReject(comment)}>
            Rejeter
          </button>
        </div>
      </div>
      <div className="mt-4 grid gap-4 md:grid-cols-2">
        <pre className="whitespace-pre-wrap rounded-2xl border border-slate-700 bg-slate-950 p-4 text-sm text-slate-100">
          {JSON.stringify(scene, null, 2)}
        </pre>
        <div className="space-y-3">
          <input
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="Commentaire"
          />
          <textarea
            className="min-h-40 w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-xs text-slate-100"
            value={edited}
            onChange={(e) => setEdited(e.target.value)}
            placeholder="Version modifiée"
          />
        </div>
      </div>
    </div>
  )
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
  const [storyboardScenes, setStoryboardScenes] = useState<Scene[]>([])
  const [storyboardApproved, setStoryboardApproved] = useState(false)
  const [characterPrompts, setCharacterPrompts] = useState<any[]>([])
  const [backgroundPrompts, setBackgroundPrompts] = useState<any[]>([])
  const [batchResult, setBatchResult] = useState<any>(null)
  const [storyboardMeta, setStoryboardMeta] = useState<{ item_slug: string; book_slug: string; visual_style_id: string } | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    listBooks().then((r) => r.ok && setBooks(r.books))
    listImageStyles().then((r) => r.ok && setStyles(r.styles))
  }, [])

  const allStoryboardScenesReady =
    storyboardScenes.length > 0 && storyboardScenes.every((scene) => scene.status === 'approved' || scene.status === 'edited')
  const allCharacterPromptsApproved = characterPrompts.length > 0 && characterPrompts.every((prompt) => prompt.status === 'approved')
  const allBackgroundPromptsApproved = backgroundPrompts.length > 0 && backgroundPrompts.every((prompt) => prompt.status === 'approved')
  const currentStyle = useMemo(() => styles.find((style) => style.id === form.visual_style_id) ?? null, [form.visual_style_id, styles])

  async function generateStoryboard() {
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
    if (!response.ok) {
      setError(getFriendlyErrorMessage(response.error.code, response.error.message))
      return
    }
    setStoryboardApproved(false)
    setCharacterPrompts([])
    setBackgroundPrompts([])
    setBatchResult(null)
    setStoryboardMeta({
      item_slug: response.item_slug,
      book_slug: response.book_slug,
      visual_style_id: response.visual_style_id,
    })
    setStoryboardScenes((response.storyboard?.scenes ?? []).map((scene: any) => ({ ...scene, status: 'pending' })))
  }

  async function approveStoryboard() {
    if (!storyboardMeta) return
    const response = await approveImageStoryboard({
      item_slug: storyboardMeta.item_slug,
      book_slug: storyboardMeta.book_slug,
      visual_style_id: storyboardMeta.visual_style_id,
      storyboard: { scenes: storyboardScenes },
    })
    if (!response.ok) {
      setError(getFriendlyErrorMessage(response.error.code, response.error.message))
      return
    }
    setStoryboardApproved(true)
  }

  async function generateCharacterPrompts() {
    if (!storyboardMeta) return
    const response = await generateImageCharacterPrompts({
      item_slug: storyboardMeta.item_slug,
      book_slug: storyboardMeta.book_slug,
      visual_style_id: storyboardMeta.visual_style_id,
      storyboard: { scenes: storyboardScenes },
      provider: form.provider,
      model: form.provider === 'openai' ? form.model : null,
      temperature: Number(form.temperature),
      hitl_enabled: form.hitl_enabled,
      export_formats: [],
    })
    if (response.ok) setCharacterPrompts(response.character_prompts)
  }

  async function generateBackgroundPrompts() {
    if (!storyboardMeta) return
    const response = await generateImageBackgroundPrompts({
      item_slug: storyboardMeta.item_slug,
      book_slug: storyboardMeta.book_slug,
      visual_style_id: storyboardMeta.visual_style_id,
      storyboard: { scenes: storyboardScenes },
      character_prompts: characterPrompts,
      provider: form.provider,
      model: form.provider === 'openai' ? form.model : null,
      temperature: Number(form.temperature),
      hitl_enabled: form.hitl_enabled,
      export_formats: [],
    })
    if (response.ok) setBackgroundPrompts(response.background_prompts)
  }

  async function generateBatch() {
    if (!storyboardMeta) return
    const response = await generateImageBatch({
      item_slug: storyboardMeta.item_slug,
      storyboard: { scenes: storyboardScenes },
      character_prompts: characterPrompts,
      background_prompts: backgroundPrompts,
      backend: 'mock',
      confirm_generation: true,
    })
    if (response.ok) setBatchResult(response)
  }

  function updateScene(sceneId: string, next: Partial<Scene>) {
    setStoryboardScenes((current) => current.map((scene) => (scene.scene_id === sceneId ? { ...scene, ...next } : scene)))
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold text-slate-100">Image</h1>
        <p className="max-w-3xl text-sm text-slate-400">Workflow storyboard puis prompts, avec validation locale des scènes et validation globale du storyboard.</p>
      </div>

      <form
        className="panel grid gap-4 rounded-3xl p-6"
        onSubmit={async (event) => {
          event.preventDefault()
          await generateStoryboard()
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
              <option value="4:5">4:5</option>
              <option value="1:1">1:1</option>
              <option value="9:16">9:16</option>
              <option value="16:9">16:9</option>
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

      {storyboardScenes.length > 0 ? (
        <section className="space-y-4">
          <div className="flex flex-wrap gap-2">
            <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-100">1. Storyboard généré</span>
            <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-100">2. Scènes validées</span>
            <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-100">3. Storyboard OK</span>
            <span className="rounded-full bg-slate-800 px-3 py-1 text-sm text-slate-100">4. Prompts personnages</span>
          </div>
          {storyboardScenes.map((scene) => (
            <ImageStoryboardSceneCard
              key={scene.scene_id}
              scene={scene}
              onApprove={() => updateScene(scene.scene_id, { status: 'approved' })}
              onReject={(comment) => updateScene(scene.scene_id, { status: 'rejected', comment })}
              onEdit={(edited, comment) => {
                try {
                  const parsed = JSON.parse(edited) as Scene
                  updateScene(scene.scene_id, { ...parsed, status: 'edited', comment })
                } catch {
                  updateScene(scene.scene_id, { status: 'edited', comment })
                }
              }}
            />
          ))}
        </section>
      ) : null}

      {storyboardScenes.length > 0 && allStoryboardScenesReady && !storyboardApproved ? (
        <button className="rounded-xl bg-sky-500 px-4 py-2 text-slate-950" onClick={approveStoryboard} type="button">
          Storyboard OK — passer aux prompts personnages
        </button>
      ) : null}

      {storyboardApproved ? <div className="rounded-2xl border border-emerald-700 bg-emerald-950/40 px-4 py-3 text-emerald-200">Storyboard validé</div> : null}

      {storyboardApproved ? (
        <section className="space-y-4">
          <div className="panel rounded-3xl p-6">
            <h2 className="text-lg font-semibold text-slate-50">Prompts personnages</h2>
            <button type="button" className="mt-3 rounded-xl bg-sky-500 px-4 py-2 text-slate-950" onClick={generateCharacterPrompts}>
              Générer les prompts personnages
            </button>
            {characterPrompts.length > 0 ? <pre className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm">{JSON.stringify(characterPrompts, null, 2)}</pre> : null}
          </div>

          {allCharacterPromptsApproved ? (
            <div className="panel rounded-3xl p-6">
              <h2 className="text-lg font-semibold text-slate-50">Prompts décors</h2>
              <button type="button" className="mt-3 rounded-xl bg-sky-500 px-4 py-2 text-slate-950" onClick={generateBackgroundPrompts}>
                Générer les prompts décors
              </button>
              {backgroundPrompts.length > 0 ? <pre className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm">{JSON.stringify(backgroundPrompts, null, 2)}</pre> : null}
            </div>
          ) : null}

          {allCharacterPromptsApproved && allBackgroundPromptsApproved ? (
            <div className="panel rounded-3xl p-6">
              <h2 className="text-lg font-semibold text-slate-50">Génération batch</h2>
              <button type="button" className="mt-3 rounded-xl bg-emerald-500 px-4 py-2 text-slate-950" onClick={generateBatch}>
                Générer les images en lot
              </button>
              {batchResult ? <pre className="mt-3 rounded-xl border border-slate-800 bg-slate-950 p-3 text-sm">{JSON.stringify(batchResult.images, null, 2)}</pre> : null}
            </div>
          ) : null}
        </section>
      ) : null}
    </div>
  )
}
