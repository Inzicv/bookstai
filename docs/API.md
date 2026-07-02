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
- `GET /image/styles`
- `POST /image/run`
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

- le contexte;
- la comedy room;
- la chanson parodique;
- le storyboard;
- les prompts personnages;
- les prompts backgrounds;
- le texte social.

`POST /song/run` attend:

```json
{
  "book_slug": "lesheritiersdorion",
  "story_scope": "pitch_only",
  "song_style": "parody",
  "platform": "tiktok",
  "provider": "mock",
  "model": null,
  "temperature": 0.7,
  "hitl_enabled": true
}
```

`story_scope` peut valoir `pitch_only` ou `full_spoilers`.
`song_style` vaut actuellement `parody`.
`platform` vaut `tiktok` ou `instagram`.
`provider` vaut `mock`.
`model` est optionnel.
`temperature` est un réglage de créativité.
`hitl_enabled` active la session HITL Song.

## Image

Le workflow Image repart de paroles de chanson déjà validées ou collées manuellement.
Il ne génère pas d’image directement.
Il produit:

- le style visuel sélectionné;
- la direction visuelle;
- le storyboard;
- les prompts personnages, backgrounds, objets et notes de style;
- les exports Markdown et/ou JSON si demandés.

`GET /image/styles` liste les styles visuels disponibles depuis `memory/visual_style/Prompts_visuels/`.

`POST /image/run` attend:

```json
{
  "lyrics": "Paroles complètes de la chanson validée...",
  "visual_style_id": "diorama_carton",
  "platform": "instagram",
  "format": "4:5",
  "brief": "Créer des visuels utilisables pour illustrer la chanson en reel.",
  "provider": "mock",
  "export_formats": ["markdown", "json"]
}
```

`platform` vaut `instagram`, `tiktok` ou `youtube_shorts`.
`format` décrit le ratio de sortie.
`brief` est optionnel.
`provider` vaut `mock` ou `openai`.
`export_formats` est optionnel et peut contenir `markdown` et/ou `json`.
Le HITL Image utilise les étapes `style_selection`, `storyboard` et `prompts`.

## Principes

- Le provider par défaut est `mock`.
- Aucun appel OpenAI n'est effectué par défaut.
- Le workflow Song ne génère pas d'image.
- Le workflow Image ne génère pas d'image non plus.
- Les références de style viennent de la mémoire BookstAI, pas d'un champ utilisateur.
- `platform` sert uniquement à l’agent Social Media.
- La CLI reste disponible mais secondaire.

## Learning Apply

`/learning/apply` refuse toute modification si `confirm` n'est pas `true`.
La mémoire `memory/` ne peut être modifiée que par cette route et avec confirmation explicite.
