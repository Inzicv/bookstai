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

## Custom Component Langflow

Objectif :
Utiliser BookstAI Review directement dans Langflow.

Prérequis :
- BookstAI installé en editable install
- Langflow installé localement
- être à la racine du dépôt BookstAI

Fichier composant :
`langflow_components/bookstai_review_component.py`

Entrées :
- `book_slug`
- `user_opinion`
- `platform`
- `provider`
- `model`
- `temperature`
- `memory_root`
- `prompt_root`

Sortie :
Dictionnaire complet du `ReviewWorkflow`.

Limites :
- mocks uniquement par défaut
- aucun appel OpenAI tant que `provider` vaut `mock`
- pas encore de validation humaine entre les étapes

### Vérification manuelle

1. Lancer Langflow.
2. Ajouter le dossier `langflow_components` comme source de Custom Components.
3. Ajouter le composant `BookstAIReviewComponent` dans un flow.
4. Renseigner :
   - `book_slug`
   - `user_opinion`
   - `platform`
5. Exécuter le composant.
6. Vérifier que la sortie contient :
   - `workflow`
   - `book_slug`
   - `context`
   - `style`
   - `comedy`
   - `review`
   - `social`

## Epic 2 — Song Workflow avec mocks

Objectif :
Permettre à Langflow d'exécuter le workflow Song existant sans appel OpenAI et sans backend image réel.

Entrées :
- `book_slug`
- `spoiler_mode`
- `prompt_type`
- `platform`
- `provider`
- `model`
- `temperature`
- `memory_root`
- `prompt_root`
- `image_path`

Sortie :
Dictionnaire complet du `SongWorkflow`.

Limites :
- utilise `MockImageBackend`
- aucun appel API image réel
- pas encore de Human In The Loop Langflow

## Import Python

```python
from bookstai.langflow.song_component import run_song_workflow

result = run_song_workflow(
    book_slug="example",
    spoiler_mode="spoiler_free",
    prompt_type="thumbnail",
    platform="tiktok",
)
```

## Custom Component Langflow — Song

Objectif :
Utiliser BookstAI Song directement dans Langflow.

Prérequis :
- BookstAI installé en editable install
- Langflow installé localement
- être à la racine du dépôt BookstAI

Fichier composant :
`langflow_components/bookstai_song_component.py`

Entrées :
- `book_slug`
- `spoiler_mode`
- `prompt_type`
- `platform`
- `provider`
- `model`
- `temperature`
- `memory_root`
- `prompt_root`
- `image_path`

Sortie :
Dictionnaire complet du `SongWorkflow`.

Limites :
- mocks uniquement par défaut
- `MockImageBackend`
- aucun appel OpenAI tant que `provider` vaut `mock`
- aucune génération d'image réelle
- pas encore de validation humaine entre les étapes

### Vérification manuelle

1. Lancer Langflow.
2. Ajouter le dossier `langflow_components` comme source de Custom Components.
3. Ajouter le composant `BookstAISongComponent` dans un flow.
4. Renseigner :
   - `book_slug`
   - `spoiler_mode`
   - `prompt_type`
   - `platform`
5. Exécuter le composant.
6. Vérifier que la sortie contient :
   - `workflow`
   - `book_slug`
   - `context`
   - `style`
   - `comedy`
   - `song`
   - `art_direction`
   - `image_prompt`
   - `image`
   - `social`

## OpenAI dans Langflow

Les composants Langflow BookstAI peuvent utiliser OpenAI via les champs :

- `provider`
- `model`
- `temperature`

Par défaut, `provider` vaut `mock`.

Pour activer OpenAI :

1. installer BookstAI avec l'extra OpenAI ;
2. définir `OPENAI_API_KEY` dans l'environnement qui exécute Langflow ;
3. ouvrir le composant BookstAI dans Langflow ;
4. définir `provider` à `openai` ;
5. choisir le modèle ;
6. exécuter le flow.

La clé API ne doit jamais être saisie directement dans Langflow.

Le provider `mock` doit être utilisé pour les tests, les démos et les essais sans coût.

## Images locales dans Langflow

Pour l’instant, les workflows Langflow utilisent encore `MockImageBackend`.

Le futur backend image local sera branché derrière l’interface `ImageBackend`.

L’objectif est de permettre ensuite à Langflow de choisir :

- `mock`
- `comfyui`

OpenAI ne sera pas utilisé pour générer les images.

La génération image locale sera traitée dans un Epic dédié.
