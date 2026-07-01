const API_URL = process.env.NEXT_PUBLIC_BOOKSTAI_API_URL ?? 'http://127.0.0.1:8000'

type ApiError = { ok: false; error: { code: string; message: string } }
type ApiSuccess<T> = T & { ok: true }

export type HealthResponse = {
  status: string
  app: string
  mode: string
}

export type ReviewRunResponse = ApiSuccess<{
  type: 'review'
  book_slug: string
  provider: 'mock'
  hitl_enabled: boolean
  result: Record<string, unknown>
  hitl_session_path: string | null
}>

export type SongRunResponse = ApiSuccess<{
  type: 'song'
  book_slug: string
  provider: 'mock'
  image_backend: 'mock'
  hitl_enabled: boolean
  result: Record<string, unknown>
  hitl_session_path: string | null
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

async function request<T>(path: string, init?: RequestInit): Promise<T | ApiError> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  })
  const data = await response.json()
  if (!response.ok || data?.ok === false) return data
  return data
}

export async function getHealth() {
  const response = await fetch(`${API_URL}/health`)
  if (!response.ok) throw new Error('API indisponible')
  return response.json() as Promise<HealthResponse>
}

export const runReview = (payload: unknown) =>
  request<ReviewRunResponse>('/review/run', { method: 'POST', body: JSON.stringify(payload) })
export const runSong = (payload: unknown) =>
  request<SongRunResponse>('/song/run', { method: 'POST', body: JSON.stringify(payload) })
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
