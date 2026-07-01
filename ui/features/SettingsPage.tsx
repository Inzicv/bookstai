import { getApiBaseUrl } from '@/lib/api'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-semibold text-slate-100">Settings</h1>
      <div className="panel space-y-3 rounded-3xl p-6">
        <p className="text-slate-300">
          API utilisée: <code className="rounded bg-slate-800 px-2 py-1 text-slate-100">{getApiBaseUrl()}</code>
        </p>
        <p className="text-slate-300">
          Provider par défaut: <code className="rounded bg-slate-800 px-2 py-1 text-slate-100">mock</code>
        </p>
        <p className="text-slate-300">
          Image backend par défaut: <code className="rounded bg-slate-800 px-2 py-1 text-slate-100">mock</code>
        </p>
        <p className="text-slate-300">OpenAI non activé dans cette epic.</p>
        <p className="text-slate-300">Aucune clé API côté frontend.</p>
        <p className="text-slate-300">Langflow retiré du projet.</p>
      </div>
    </div>
  )
}
