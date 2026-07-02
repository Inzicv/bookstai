# Architecture

Source de vérité:

`memory/books/*.md`

## Architecture locale

- UI locale Next.js
- API locale FastAPI
- workflows Python BookstAI

## Principes

- les fichiers Markdown sont maintenus manuellement;
- ils sont consommés directement par les assistants spécialisés;
- Human In The Loop partout où une validation humaine est utile;
- pas de dépendance active à Langflow;
- pas de génération d'image dans le workflow Song.
- le workflow Image est séparé du workflow Song et repart des paroles validées.

## Références mémoire principales

- `memory/books/<livre>.md`
- `memory/reviews/reviews.md`
- `memory/humor/references.md`
- `memory/songs/`
- `memory/visual_style/`
- `memory/visual_style/Prompts_visuels/`

## HITL

BookstAI utilise un socle HITL pour représenter les étapes créatives à valider.

Une étape HITL peut être:

- `pending`
- `approved`
- `rejected`
- `edited`

Le contenu original généré par l'IA doit toujours rester disponible.

Quand l'utilisateur corrige une sortie, la version corrigée est stockée séparément dans `edited_content`.

## HITL dans le workflow Review

Les étapes créatives à valider sont:

- `comedy`
- `review`
- `social`

## HITL dans le workflow Song

Les étapes créatives à valider sont:

- `song`
- `song_options`

Song ne génère pas d'image.

## HITL dans le workflow Image

Les étapes créatives à valider sont:

- `style_selection`
- `storyboard`
- `prompts`

Le workflow Image repart d'une chanson existante et d'un style visuel sélectionné.

## Learning Loop

La Learning Loop extrait des sessions HITL et prépare un brouillon Markdown avant toute application.

Seules les étapes validées ou éditées sont exploitables.

La mémoire n'est jamais modifiée automatiquement.

## Persistance HITL

Les sessions HITL peuvent être sauvegardées en JSON dans:

```text
outputs/hitl/<workflow_name>/<item_slug>.json
```

Le JSON conserve:

- le nom du workflow;
- le slug du livre;
- les étapes HITL;
- le statut de chaque étape;
- le contenu original;
- le contenu édité si disponible;
- les commentaires éventuels;
- les métadonnées.
