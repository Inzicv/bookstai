export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Settings</h1>
      <div className="panel rounded-3xl p-6 space-y-3">
        <p>API utilisée: <code className="rounded bg-zinc-100 px-2 py-1">http://127.0.0.1:8000</code></p>
        <p>Provider par défaut: <code className="rounded bg-zinc-100 px-2 py-1">mock</code></p>
        <p>Image backend par défaut: <code className="rounded bg-zinc-100 px-2 py-1">mock</code></p>
        <p>OpenAI non activé dans cette epic.</p>
        <p>Aucune clé API côté frontend.</p>
      </div>
    </div>
  )
}

