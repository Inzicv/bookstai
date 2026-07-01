'use client'

import { useEffect, useState } from 'react'
import { listBooks, type BookListItem } from '@/lib/api'
import { FormField } from '@/components/FormField'

export function BookSelect({
  value,
  onChange,
}: {
  value: string
  onChange: (slug: string) => void
}) {
  const [books, setBooks] = useState<BookListItem[]>([])
  useEffect(() => {
    listBooks().then((response) => {
      if (response.ok) setBooks(response.books)
    })
  }, [])
  return (
    <FormField label="Livre">
      <select className="w-full rounded-xl border border-slate-700 bg-slate-950 px-3 py-2 text-slate-100" value={value} onChange={(e) => onChange(e.target.value)}>
        <option value="">Choisir un livre</option>
        {books.map((book) => (
          <option key={book.slug} value={book.slug}>
            {book.title} ({book.slug})
          </option>
        ))}
      </select>
    </FormField>
  )
}
