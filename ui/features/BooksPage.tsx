'use client'

import { useEffect, useState } from 'react'
import { createBook, getBook, listBooks, updateBook, type BookListItem } from '@/lib/api'
import { ErrorMessage } from '@/components/ErrorMessage'
import { LoadingButton } from '@/components/LoadingButton'
import { FormField } from '@/components/FormField'
import { BookSlugField } from '@/components/BookSlugField'

export default function BooksPage() {
  const [books, setBooks] = useState<BookListItem[]>([])
  const [editingSlug, setEditingSlug] = useState<string | null>(null)
  const [slug, setSlug] = useState('')
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [message, setMessage] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const refresh = async () => {
    const response = await listBooks()
    if (response.ok) setBooks(response.books)
  }

  useEffect(() => {
    refresh()
  }, [])

  const loadBook = async (slug: string) => {
    setEditingSlug(slug)
    setSlug(slug)
    if (!slug) {
      setTitle('')
      setContent('')
      return
    }
    const response = await getBook(slug)
    if (!response.ok) {
      setError(response.error.message)
      return
    }
    setTitle(response.book.title)
    setContent(response.book.content)
  }

  return (
    <div className="space-y-6">
      <div className="space-y-2">
        <h1 className="text-3xl font-semibold text-slate-100">Livres</h1>
        <p className="max-w-2xl text-sm text-slate-300">
          Crée et modifie localement les fiches Markdown utilisées ensuite par Review et Song.
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-[0.9fr_1.1fr]">
        <section className="panel rounded-3xl p-6">
          <div className="mb-4 text-sm uppercase tracking-[0.18em] text-slate-400">Bibliothèque</div>
          <div className="space-y-2">
            {books.length === 0 ? (
              <div className="rounded-2xl border border-dashed border-slate-800 px-4 py-6 text-sm text-slate-400">
                Aucun livre pour le moment.
              </div>
            ) : (
              books.map((book) => (
                <button
                  key={book.slug}
                  type="button"
                  className={`w-full rounded-2xl border px-4 py-3 text-left transition ${
                    editingSlug === book.slug
                      ? 'border-violet-400/40 bg-violet-500/10'
                      : 'border-slate-800 bg-slate-950/40 hover:bg-slate-900'
                  }`}
                  onClick={() => void loadBook(book.slug)}
                >
                  <div className="font-medium text-slate-100">{book.title}</div>
                  <div className="text-xs text-slate-400">{book.slug}</div>
                  <div className="text-xs text-slate-500">{book.path}</div>
                </button>
              ))
            )}
          </div>
        </section>

        <section className="panel rounded-3xl p-6">
          <div className="mb-4 text-sm uppercase tracking-[0.18em] text-slate-400">Fiche Markdown</div>
          <form
            className="space-y-4"
            onSubmit={async (event) => {
              event.preventDefault()
              setLoading(true)
              setError(null)
              setMessage(null)
              const payload = { title, slug, content }
              const response = editingSlug ? await updateBook(editingSlug, { title, content }) : await createBook(payload)
              setLoading(false)
              if (!response.ok) {
                setError(response.error.message)
                return
              }
              setMessage(`Fiche enregistrée. Tu peux maintenant utiliser ce slug dans Review ou Song.`)
              await refresh()
              setEditingSlug(response.book.slug)
              setSlug(response.book.slug)
            }}
          >
            <BookSlugField
              title={title}
              slug={slug}
              autoGenerateSlug={!editingSlug}
              onTitleChange={setTitle}
              onSlugChange={setSlug}
            />
            <FormField label="Fiche Markdown">
              <textarea
                className="min-h-[280px] w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 font-mono text-sm text-slate-100"
                placeholder={`# Titre du livre\n\n### 1. Personnages\n\n* **Nom Prénom**\n  * **Espèce :** ...`}
                value={content}
                onChange={(e) => setContent(e.target.value)}
              />
            </FormField>
            <div className="flex flex-wrap gap-3">
              <LoadingButton loading={loading}>Enregistrer la fiche</LoadingButton>
              <button
                type="button"
                className="rounded-xl border border-slate-700 px-4 py-2 text-sm text-slate-200"
                onClick={() => {
                  setEditingSlug(null)
                  setSlug('')
                  setTitle('')
                  setContent('')
                  setError(null)
                  setMessage(null)
                }}
              >
                Nouvelle fiche
              </button>
            </div>
          </form>
          {message ? <div className="mt-4 rounded-2xl border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm text-emerald-100">{message}</div> : null}
          {error ? <div className="mt-4"><ErrorMessage message={error} /></div> : null}
        </section>
      </div>
    </div>
  )
}
