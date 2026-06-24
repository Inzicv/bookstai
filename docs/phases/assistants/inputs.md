# Entrées des assistants spécialisés

Principe :

- une seule fiche livre active à la fois ;
- les assistants lisent directement les fichiers Markdown existants ;
- pas de couche de transformation obligatoire ;
- pas de JSON, pas de base vectorielle, pas de moteur de recherche généraliste.

## Review Assistant

Entrées :

- `memory/books/<slug>.md`
- `memory/reviews/reviews.md`
- `memory/humor/references.md`

But :

- produire une review, une accroche, un avis, des angles de communication.

## Song Assistant

Entrées :

- `memory/books/<slug>.md`
- `memory/songs/`
- `memory/humor/references.md`

But :

- générer des idées de paroles, rimes, structures, références.

## Art Director

Entrées :

- `memory/books/<slug>.md`
- `memory/visual_style/`

But :

- produire des prompts image, des directions visuelles, des concepts de couverture ou storyboard.

## Comedy Room

Entrées :

- `memory/books/<slug>.md`
- `memory/reviews/reviews.md`
- `memory/humor/references.md`

But :

- produire hooks, analogies, blagues, punchlines, références.

## Règle d'or

Avant toute nouvelle couche technique, se poser la question :

« Est-ce que cela me fait réellement gagner du temps ? »

Si la réponse est non, on reste sur les Markdown existants.
