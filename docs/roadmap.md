# Roadmap

## Architecture officielle

Next.js UI
↓
FastAPI API
↓
Python workflows

## Epic 8.1

- API FastAPI locale.
- Routes Review, Song, HITL et Learning.
- Provider par défaut `mock`.
- Learning Apply avec confirmation explicite.
- Tests mock sans appel OpenAI.
- Documentation locale mise à jour.

## Epic 8.2

- UI Next.js locale dans `ui/`.
- Accueil, Review, Song, HITL, Learning, Settings.
- Client API branché sur `NEXT_PUBLIC_BOOKSTAI_API_URL`.
- Confirmation explicite avant `POST /learning/apply`.
- Aucun secret ou clé OpenAI côté frontend.
- Interface simple, lisible et utilisable en local.

## Epic 8.3

- Workflow Song refondu autour de:
  - Context Builder
  - Comedy Room
  - Song Writer
  - HITL chanson
  - Art Director
  - HITL storyboard
  - Prompt Maker
  - Social Media
- Le workflow Song ne génère pas d'image.
- La sortie Song expose chanson, storyboard, prompts et social.
