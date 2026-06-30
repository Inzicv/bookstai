# Langflow Integration

## Epic 1 — Review Workflow avec mocks

Objectif :
Permettre à Langflow d'exécuter le workflow Review existant sans appel OpenAI.

Entrées :
- `book_slug`
- `user_opinion`
- `platform`
- `memory_root`
- `prompt_root`

Sortie :
Dictionnaire complet du `ReviewWorkflow`.

Limites :
- utilise `MockLLMClient`
- aucun appel API
- aucune génération d'image
- pas encore de Human In The Loop Langflow

## Import Python

```python
from bookstai.langflow.review_component import run_review_workflow

result = run_review_workflow(
    book_slug="example",
    user_opinion="J'ai aimé l'ambiance et les personnages.",
    platform="tiktok",
)
```

## Paramètres

- `book_slug`: slug du livre à charger depuis `memory_root/books`.
- `user_opinion`: avis utilisateur transmis au workflow.
- `platform`: plateforme sociale utilisée par le workflow.
- `memory_root`: racine des fichiers mémoire, accepte `str` ou `Path`.
- `prompt_root`: racine des prompts, accepte `str` ou `Path`.

## Résultat attendu

Le composant retourne directement le dictionnaire produit par `ReviewWorkflow.run(...)`, avec au minimum :

- `workflow`
- `book_slug`
- `context`
- `style`
- `comedy`
- `review`
- `social`

## Utilisation dans Langflow

Importez la fonction `run_review_workflow` comme point d'entrée Python dans un composant Langflow.
Le composant agit comme un adaptateur fin autour du workflow existant.
