# BookstAI local app

BookstAI expose une API FastAPI locale pour piloter les workflows existants.

Lancement:

```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Comportement attendu:

- mode local uniquement;
- `mock` comme provider par défaut;
- pas d'appel OpenAI par défaut;
- aucune écriture automatique dans `memory/`;
- les sessions HITL et les brouillons Learning sont stockés sous `outputs/`.

