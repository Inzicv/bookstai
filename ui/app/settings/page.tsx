import { getApiBaseUrl } from '@/lib/api'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold">Settings</h1>
      <div className="panel space-y-3 rounded-3xl p-6">
        <p>
          API utilisée: <code className="rounded bg-zinc-100 px-2 py-1">{getApiBaseUrl()}</code>
        </p>
        <p>
          provider par défaut = <code className="rounded bg-zinc-100 px-2 py-1">mock</code>
        </p>
        <p>
          image backend par défaut = <code className="rounded bg-zinc-100 px-2 py-1">mock</code>
        </p>
        <p>OpenAI non activé dans cette epic.</p>
        <p>aucune clé API côté frontend.</p>
        <p>Langflow retiré du projet.</p>
      </div>
    </div>
  )
}
