# Architecture

Source de vérité :

`memory/books/*.md`

Principe général :

- les fichiers Markdown sont maintenus manuellement ;
- ils sont consommés directement par les assistants spécialisés ;
- aucun agent intermédiaire n'est chargé de gérer les livres ;
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
