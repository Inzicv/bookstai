'use client'

import { useEffect, useMemo, useState } from 'react'
import { listBooks, type BookListItem } from '@/lib/api'
import { FormField } from '@/components/FormField'

function slugify(value: string) {
  return value
    .toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .replace(/-{2,}/g, '-')
}

export function BookSlugField({
  title,
  slug,
  autoGenerateSlug,
  onTitleChange,
  onSlugChange,
}: {
  title: string
  slug: string
  autoGenerateSlug: boolean
  onTitleChange: (value: string) => void
  onSlugChange: (value: string) => void
}) {
  const [books, setBooks] = useState<BookListItem[]>([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    let mounted = true
    setLoading(true)
    listBooks()
      .then((response) => {
        if (mounted && response.ok) setBooks(response.books)
      })
      .finally(() => {
        if (mounted) setLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  const suggestions = useMemo(() => books.map((book) => book.slug), [books])

  return (
    <div className="grid gap-4 md:grid-cols-2">
      <FormField label="Nom du livre">
        <input
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
          value={title}
          onChange={(e) => {
            const nextTitle = e.target.value
            onTitleChange(nextTitle)
            if (autoGenerateSlug) onSlugChange(slugify(nextTitle))
          }}
        />
      </FormField>
      <FormField label="Slug">
        <input
          className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100"
          list="book-slugs"
          value={slug}
          onChange={(e) => onSlugChange(e.target.value)}
        />
        <datalist id="book-slugs">
          {suggestions.map((suggestion) => (
            <option key={suggestion} value={suggestion} />
          ))}
        </datalist>
        <p className="text-xs text-slate-400">
          Le slug sert d'identifiant technique. Il créera le fichier memory/books/slug.md.
        </p>
        {loading ? <p className="text-xs text-slate-500">Chargement des livres existants...</p> : null}
      </FormField>
    </div>
  )
}
