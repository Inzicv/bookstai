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

## Song

Le workflow Song ne génère pas d'image.
Il produit:

- la chanson parodique;
- le storyboard vidéo réalisable;
- les prompts personnages;
- les prompts backgrounds;
- le texte social.

`POST /song/run` attend:

```json
{
  "book_slug": "lesheritiersdorion",
  "story_scope": "pitch_only",
  "song_style": "parody",
  "reference_song": "Mockingbird - Eminem",
  "platform": "tiktok",
  "provider": "mock",
  "model": null,
  "temperature": 0.7,
  "hitl_enabled": true
}
```

`story_scope` peut valoir `pitch_only` ou `full_spoilers`.

## Principes

- Le provider par défaut est `mock`.
- Aucun appel OpenAI n'est effectué par défaut.
- Le workflow Song ne génère pas d'image.
- La CLI reste disponible mais secondaire.

## Learning Apply

`/learning/apply` refuse toute modification si `confirm` n'est pas `true`.
La mémoire `memory/` ne peut être modifiée que par cette route et avec confirmation explicite.
