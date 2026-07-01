# BookstAI local app

BookstAI expose une API FastAPI locale et une UI Next.js locale pour piloter les workflows existants.

Lancement de l'API, terminal 1:

```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Lancement de l'UI, terminal 2:

```bash
cd ui
npm install
npm run dev
```

Ouvrir:

```text
http://localhost:3000
```

Configuration frontend:

```text
NEXT_PUBLIC_BOOKSTAI_API_URL=http://127.0.0.1:8000
```

Comportement attendu:

- mode local uniquement;
- `mock` comme provider par défaut;
- pas d'appel OpenAI par défaut;
- aucune clé API côté frontend;
- aucune écriture automatique dans `memory/`;
- les sessions HITL et les brouillons Learning sont stockés sous `outputs/`.
