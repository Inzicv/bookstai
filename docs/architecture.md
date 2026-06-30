# Architecture

Source de vérité :

`memory/books/*.md`

Principe général :

- les fichiers Markdown sont maintenus manuellement ;
- ils sont consommés directement par les assistants spécialisés ;
- Human In The Loop partout.

Flux global :

Fichiers mémoire
↓
Assistants spécialisés
↓
Validation humaine
↓
Contenus finaux

Références mémoire principales :

- `memory/books/<livre>.md`
- `memory/reviews/reviews.md`
- `memory/humor/references.md`
- `memory/songs/`
- `memory/visual_style/`

Objectif :

- rester simple ;
- éviter les couches inutiles ;
- préserver la rapidité d'usage ;
- garder l'architecture alignée avec le workflow agen.

## Human In The Loop

BookstAI utilise un socle HITL pour représenter les étapes créatives à valider.

Une étape HITL peut être :

- `pending` ;
- `approved` ;
- `rejected` ;
- `edited`.

Le contenu original généré par l'IA doit toujours rester disponible.

Quand l'utilisateur corrige une sortie, la version corrigée est stockée séparément dans `edited_content`.

Le HITL ne remplace pas les workflows existants.

Il sert d'abord à structurer les validations avant l'ajout d'une UI ou d'un mode interactif.

## HITL dans le workflow Song

`SongWorkflow.run(...)` conserve le comportement historique.

`SongWorkflow.run_with_hitl(...)` exécute le même workflow, mais ajoute une session HITL.

Les étapes créatives à valider sont :

- `comedy`
- `song`
- `art_direction`
- `image_prompt`
- `image`
- `social`

Les étapes techniques comme `context` et `style` ne sont pas encore validées manuellement.
