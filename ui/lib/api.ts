const DEFAULT_API_URL = 'http://127.0.0.1:8000'

export function getApiBaseUrl() {
  return process.env.NEXT_PUBLIC_BOOKSTAI_API_URL ?? DEFAULT_API_URL
}

export type ApiFailure = { ok: false; error: { code: string; message: string } }
export type ApiSuccess<T> = T & { ok: true }

export type HealthResponse = {
  status: string
  app: string
  mode: string
}

export type ReviewRunResponse = ApiSuccess<{
  type: 'review'
  book_slug: string
  provider: 'mock' | 'openai'
  hitl_enabled: boolean
  result: Record<string, unknown>
  hitl_session_path: string | null
}>

export type SongRunResponse = ApiSuccess<{
  type: 'song'
  book_slug: string
  story_scope: 'pitch_only' | 'full_spoilers'
  song_style: 'parody'
  provider: 'mock' | 'openai'
  model: string | null
  temperature: number
  hitl_enabled: boolean
  result: Record<string, unknown>
  hitl_session_path: string | null
}>

export type ImageStyleItem = {
  id: string
  name: string
  source_path: string
  instructions: string
  sections: Record<string, string>
}

export type ImageStylesResponse = ApiSuccess<{
  styles: ImageStyleItem[]
}>

export type ImageRunResponse = ApiSuccess<{
  type: 'visual'
  book_slug: string
  item_slug: string
  visual_style_id: string
  provider: 'mock' | 'openai'
  model: string | null
  temperature: number
  hitl_enabled: boolean
  result: Record<string, unknown>
  hitl_session_path: string | null
  export_paths: Record<string, string> | null
}>

export type ImageStoryboardResponse = ApiSuccess<{
  workflow: 'visual'
  stage: 'storyboard'
  book_slug: string
  item_slug: string
  visual_style_id: string
  visual_style: Record<string, unknown>
  book_context: Record<string, unknown>
  lyrics: string
  format: string
  brief: string
  storyboard: { scenes: Array<Record<string, unknown>> }
  hitl: Record<string, unknown> | null
}>

export type ImageCharacterPromptsResponse = ApiSuccess<{
  workflow: 'visual'
  stage: 'character_prompts'
  book_slug: string
  item_slug: string
  visual_style_id: string
  character_prompts: Array<Record<string, unknown>>
  hitl: Record<string, unknown> | null
}>

export type ImageBackgroundPromptsResponse = ApiSuccess<{
  workflow: 'visual'
  stage: 'background_prompts'
  book_slug: string
  item_slug: string
  visual_style_id: string
  background_prompts: Array<Record<string, unknown>>
  hitl: Record<string, unknown> | null
}>

export type ImageBatchGenerationResponse = ApiSuccess<{
  workflow: 'visual'
  stage: 'batch'
  item_slug: string
  backend: 'mock' | 'comfyui'
  images: Array<Record<string, unknown>>
  error: { code: string; message: string } | null
}>

export type HitlSessionResponse = ApiSuccess<{
  session: {
    workflow_name: string
    item_slug: string
    steps: Array<Record<string, unknown> & { name: string; status: string }>
  }
  path: string
}>

export type LearningExtractResponse = ApiSuccess<{
  extraction: Record<string, unknown>
  path: string
}>

export type LearningDraftResponse = ApiSuccess<{
  draft_path: string
  markdown: string
}>

export type LearningApplyResponse = ApiSuccess<{
  draft_path: string
  memory_path: string
  backup_path: string | null
  applied: boolean
}>

export type BookListItem = {
  slug: string
  title: string
  path: string
}

export type BookRecord = {
  slug: string
  title: string
  content: string
}

export type BookListResponse = ApiSuccess<{
  books: BookListItem[]
}>

export type BookReadResponse = ApiSuccess<{
  book: BookRecord
}>

export type BookWriteResponse = ApiSuccess<{
  book: BookListItem
}>

async function parseResponse<T>(response: Response): Promise<T | ApiFailure> {
  const data = (await response.json().catch(() => null)) as T | ApiFailure | null
  if (!response.ok) {
    if (data && typeof data === 'object' && 'ok' in data && data.ok === false) return data
    return { ok: false, error: { code: 'HTTP_ERROR', message: `Request failed with status ${response.status}` } }
  }
  if (data && typeof data === 'object' && 'ok' in data && data.ok === false) return data
  if (data === null) {
    return { ok: false, error: { code: 'EMPTY_RESPONSE', message: 'API returned an empty response.' } }
  }
  return data as T
}

async function request<T>(path: string, init?: RequestInit): Promise<T | ApiFailure> {
  const response = await fetch(`${getApiBaseUrl()}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  return parseResponse<T>(response)
}

export async function getHealth() {
  const response = await fetch(`${getApiBaseUrl()}/health`)
  if (!response.ok) throw new Error('API indisponible')
  return (await response.json()) as HealthResponse
}

export const runReview = (payload: unknown) =>
  request<ReviewRunResponse>('/review/run', { method: 'POST', body: JSON.stringify(payload) })
export const runSong = (payload: unknown) =>
  request<SongRunResponse>('/song/run', { method: 'POST', body: JSON.stringify(payload) })
export const listImageStyles = () => request<ImageStylesResponse>('/image/styles')
export const generateImageStoryboard = (payload: unknown) =>
  request<ImageStoryboardResponse>('/image/storyboard', { method: 'POST', body: JSON.stringify(payload) })
export const generateImageCharacterPrompts = (payload: unknown) =>
  request<ImageCharacterPromptsResponse>('/image/prompts/characters', { method: 'POST', body: JSON.stringify(payload) })
export const generateImageBackgroundPrompts = (payload: unknown) =>
  request<ImageBackgroundPromptsResponse>('/image/prompts/backgrounds', { method: 'POST', body: JSON.stringify(payload) })
export const generateImageBatch = (payload: unknown) =>
  request<ImageBatchGenerationResponse>('/image/generate-batch', { method: 'POST', body: JSON.stringify(payload) })
export const runImage = (payload: unknown) =>
  request<ImageRunResponse>('/image/run', { method: 'POST', body: JSON.stringify(payload) })
export const getHitlSession = (type: string, bookSlug: string) =>
  request<HitlSessionResponse>(`/hitl/session?type=${encodeURIComponent(type)}&book_slug=${encodeURIComponent(bookSlug)}`)
export const approveHitlStep = (payload: unknown) =>
  request<HitlSessionResponse>('/hitl/approve', { method: 'POST', body: JSON.stringify(payload) })
export const rejectHitlStep = (payload: unknown) =>
  request<HitlSessionResponse>('/hitl/reject', { method: 'POST', body: JSON.stringify(payload) })
export const editHitlStep = (payload: unknown) =>
  request<HitlSessionResponse>('/hitl/edit', { method: 'POST', body: JSON.stringify(payload) })
export const extractLearning = (payload: unknown) =>
  request<LearningExtractResponse>('/learning/extract', { method: 'POST', body: JSON.stringify(payload) })
export const draftLearning = (payload: unknown) =>
  request<LearningDraftResponse>('/learning/draft', { method: 'POST', body: JSON.stringify(payload) })
export const applyLearning = (payload: unknown) =>
  request<LearningApplyResponse>('/learning/apply', { method: 'POST', body: JSON.stringify(payload) })
export const listBooks = () => request<BookListResponse>('/books')
export const getBook = (slug: string) => request<BookReadResponse>(`/books/${encodeURIComponent(slug)}`)
export const createBook = (payload: unknown) =>
  request<BookWriteResponse>('/books', { method: 'POST', body: JSON.stringify(payload) })
export const updateBook = (slug: string, payload: unknown) =>
  request<BookWriteResponse>(`/books/${encodeURIComponent(slug)}`, {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
export type SocialRunResponse = ApiSuccess<{
  type: 'social'
  book_slug: string
  provider: 'mock' | 'openai'
  result: Record<string, unknown>
}>
export const runSocial = (payload: unknown) =>
  request<SocialRunResponse>('/social/run', { method: 'POST', body: JSON.stringify(payload) })
