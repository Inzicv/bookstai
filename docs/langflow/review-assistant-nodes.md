# Langflow — Review Assistant nodes

Objectif :

Préparer le Review Assistant à être orchestré visuellement dans Langflow sans déplacer la logique métier hors de Python.

## Principe

- `memory/` reste la source de vérité ;
- Python contient la logique métier ;
- Langflow orchestre les étapes ;
- l'humain valide à chaque étape.

## Nodes disponibles

### `load_review_context(slug)`

Entrée :

- `slug` du livre actif

Sortie :

- dictionnaire avec le titre du livre, les champs utiles, les anciens `#pitch`, les anciens `#avis` et les références humoristiques

### `generate_pitch(slug)`

Entrée :

- `slug`

Sortie :

- dictionnaire avec la proposition de pitch, les idées associées, les notes et le nom de l'étape

### `generate_avis(raw_avis, validated_pitch, slug)`

Entrées :

- `raw_avis`
- `validated_pitch`
- `slug`

Sortie :

- dictionnaire avec la proposition d'avis et les entrées utiles pour l'étape suivante

### `generate_hooks(validated_pitch, validated_avis, slug)`

Entrées :

- `validated_pitch`
- `validated_avis`
- `slug`

Sortie :

- dictionnaire avec les hooks proposés

### `assemble_review_script(hook, pitch, avis, slug)`

Entrées :

- `hook`
- `pitch`
- `avis`
- `slug`

Sortie :

- dictionnaire avec le script final assemblé

## Ordre d'orchestration

1. `load_review_context`
2. `generate_pitch`
3. validation humaine
4. `generate_avis`
5. validation humaine
6. `generate_hooks`
7. validation humaine
8. `assemble_review_script`

## Remarque

Ces nodes sont des adaptateurs simples. La logique de décision reste dans les services Python.
