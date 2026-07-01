# Roadmap

## Architecture officielle

Next.js UI locale
↓
FastAPI locale
↓
Workflows Python BookstAI

## État actuel

- Provider `mock` par défaut.
- Workflow Review fonctionnel.
- Workflow Song refondu sans génération d'image.
- HITL fonctionnel dans l'UI.
- Learning Loop existante.
- Exports Markdown existants.
- Dark mode UI par défaut.
- Langflow supprimé.
- OpenAI non branché comme provider réel dans l'usage UI.
- ComfyUI préparé mais pas encore intégré comme module image complet.

## Étape 1 — Stabilisation V1 mock locale

Objectif: BookstAI V1 locale complète en `mock`.

À couvrir:

- Review UI/API.
- Song UI/API.
- HITL Review/Song.
- Learning UI/API.
- exports Markdown.
- documentation.
- tests backend.
- build UI.

## Étape 2 — OpenAI texte réel

Objectif: `provider = mock | openai`.

Contraintes:

- texte uniquement;
- clé API côté backend uniquement;
- `mock` par défaut;
- aucun appel OpenAI automatique;
- erreurs propres dans l'UI.

## Étape 3 — Module Image local ComfyUI

Objectif: créer un module image séparé.

Important:

- Song ne génère pas d'image directement.
- Song produit seulement:
  - storyboard
  - character prompts
  - background prompts

Le module Image utilisera ces prompts validés plus tard.

## Étape 4 — Provider texte local

Objectif futur: `provider = local`.

Backends possibles:

- Ollama;
- LM Studio;
- llama.cpp server;
- API locale compatible OpenAI.

## Étape 5 — Apprentissage avancé

Progression correcte:

HITL
↓
Learning Loop
↓
Mémoire structurée
↓
Dataset propre
↓
Fine-tuning éventuel

