# BookstAI API locale

Lance l'API locale avec:

```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Base URL:

```text
http://127.0.0.1:8000
```

## Routes

- `GET /health`
- `POST /review/run`
- `POST /song/run`
- `GET /hitl/session`
- `POST /hitl/approve`
- `POST /hitl/reject`
- `POST /hitl/edit`
- `POST /learning/extract`
- `POST /learning/draft`
- `POST /learning/apply`

## Principes

- Le provider par défaut est `mock`.
- Aucun appel OpenAI n'est effectué par défaut.
- L'API orchestre les services existants sous `src/bookstai/`.
- La CLI reste disponible mais secondaire.

## Learning Apply

`/learning/apply` refuse toute modification si `confirm` n'est pas `true`.
La mémoire `memory/` ne peut être modifiée que par cette route et avec confirmation explicite.

