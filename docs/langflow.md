# Langflow Integration

## Epic 1 â€” Review Workflow avec mocks

Objectif :
Permettre Ã  Langflow d'exÃ©cuter le workflow Review existant sans appel OpenAI.

EntrÃ©es :
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
- aucune gÃ©nÃ©ration d'image
- pas encore de Human In The Loop Langflow

## Import Python

```python
from bookstai.langflow.review_component import run_review_workflow

result = run_review_workflow(
    book_slug="example",
    user_opinion="J'ai aimÃ© l'ambiance et les personnages.",
    platform="tiktok",
)
```

## ParamÃ¨tres

- `book_slug`: slug du livre Ã  charger depuis `memory_root/books`.
- `user_opinion`: avis utilisateur transmis au workflow.
- `platform`: plateforme sociale utilisÃ©e par le workflow.
- `memory_root`: racine des fichiers mÃ©moire, accepte `str` ou `Path`.
- `prompt_root`: racine des prompts, accepte `str` ou `Path`.

## RÃ©sultat attendu

Le composant retourne directement le dictionnaire produit par `ReviewWorkflow.run(...)`, avec au minimum :

- `workflow`
- `book_slug`
- `context`
- `style`
- `comedy`
- `review`
- `social`

## Utilisation dans Langflow

Importez la fonction `run_review_workflow` comme point d'entrÃ©e Python dans un composant Langflow.
Le composant agit comme un adaptateur fin autour du workflow existant.

## Custom Component Langflow

Objectif :
Utiliser BookstAI Review directement dans Langflow.

PrÃ©requis :
- BookstAI installÃ© en editable install
- Langflow installÃ© localement
- Ãªtre Ã  la racine du dÃ©pÃ´t BookstAI

Fichier composant :
`langflow_components/bookstai_review_component.py`

EntrÃ©es :
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
- mocks uniquement par dÃ©faut
- aucun appel OpenAI tant que `provider` vaut `mock`
- pas encore de validation humaine entre les Ã©tapes

### VÃ©rification manuelle

1. Lancer Langflow.
2. Ajouter le dossier `langflow_components` comme source de Custom Components.
3. Ajouter le composant `BookstAIReviewComponent` dans un flow.
4. Renseigner :
   - `book_slug`
   - `user_opinion`
   - `platform`
5. ExÃ©cuter le composant.
6. VÃ©rifier que la sortie contient :
   - `workflow`
   - `book_slug`
   - `context`
   - `style`
   - `comedy`
   - `review`
   - `social`

## Epic 2 â€” Song Workflow avec mocks

Objectif :
Permettre Ã  Langflow d'exÃ©cuter le workflow Song existant sans appel OpenAI et sans backend image rÃ©el.

EntrÃ©es :
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
- aucun appel API image rÃ©el
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

## Custom Component Langflow â€” Song

Objectif :
Utiliser BookstAI Song directement dans Langflow.

PrÃ©requis :
- BookstAI installÃ© en editable install
- Langflow installÃ© localement
- Ãªtre Ã  la racine du dÃ©pÃ´t BookstAI

Fichier composant :
`langflow_components/bookstai_song_component.py`

EntrÃ©es :
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
- mocks uniquement par dÃ©faut
- `MockImageBackend`
- aucun appel OpenAI tant que `provider` vaut `mock`
- aucune gÃ©nÃ©ration d'image rÃ©elle
- pas encore de validation humaine entre les Ã©tapes

### VÃ©rification manuelle

1. Lancer Langflow.
2. Ajouter le dossier `langflow_components` comme source de Custom Components.
3. Ajouter le composant `BookstAISongComponent` dans un flow.
4. Renseigner :
   - `book_slug`
   - `spoiler_mode`
   - `prompt_type`
   - `platform`
5. ExÃ©cuter le composant.
6. VÃ©rifier que la sortie contient :
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

Par dÃ©faut, `provider` vaut `mock`.

Pour activer OpenAI :

1. installer BookstAI avec l'extra OpenAI ;
2. dÃ©finir `OPENAI_API_KEY` dans l'environnement qui exÃ©cute Langflow ;
3. ouvrir le composant BookstAI dans Langflow ;
4. dÃ©finir `provider` Ã  `openai` ;
5. choisir le modÃ¨le ;
6. exÃ©cuter le flow.

La clÃ© API ne doit jamais Ãªtre saisie directement dans Langflow.

Le provider `mock` doit Ãªtre utilisÃ© pour les tests, les dÃ©mos et les essais sans coÃ»t.

## Images locales dans Langflow

Pour lâ€™instant, les workflows Langflow utilisent encore `MockImageBackend`.

Le futur backend image local sera branchÃ© derriÃ¨re lâ€™interface `ImageBackend`.

Lâ€™objectif est de permettre ensuite Ã  Langflow de choisir :

- `mock`
- `comfyui`

OpenAI ne sera pas utilisÃ© pour gÃ©nÃ©rer les images.

La gÃ©nÃ©ration image locale sera traitÃ©e dans un Epic dÃ©diÃ©.

## RÃ©solution des chemins BookstAI

Les adaptateurs Langflow rÃ©solvent dÃ©sormais les chemins de BookstAI indÃ©pendamment du dossier courant.

Cela permet de charger les prompts et la mÃ©moire depuis lâ€™architecture rÃ©elle du projet sans demander de dossier `prompts` Ã  la racine du repo Langflow.

## Prompts projet et prÃ©-check

Les prompts agents BookstAI vivent dans :

`prompts/agents/`

Le prÃ©-check projet permet de vÃ©rifier rapidement que les prompts obligatoires sont bien prÃ©sents avant de relancer Langflow.

Il ne corrige rien automatiquement et sert uniquement Ã  diagnostiquer l'Ã©tat du projet.
## Backend image dans Langflow Song

Le composant `BookstAISongComponent` permet de choisir le backend image.

Backends disponibles :

- `mock`
- `comfyui`

Par défaut :

```text
image_backend = mock
```

Le backend mock retourne un chemin d'image fictif et ne génère aucune image réelle.

Pour préparer ComfyUI :

```text
image_backend = comfyui
comfyui_url = http://127.0.0.1:8188
comfyui_workflow_path = chemin/vers/workflow.json
image_output_dir = outputs/images
image_timeout = 60.0
image_poll_interval = 1.0
```

ComfyUI n'est jamais utilisé par défaut.

Les tests et les premiers flows doivent rester en mock.

## HITL dans Langflow

Les composants Langflow BookstAI exposent un champ `hitl`.

Par défaut :

```text
hitl = false
```

Quand `hitl` est désactivé, les composants utilisent le comportement historique.

Quand `hitl` est activé, les composants appellent `run_with_hitl(...)` et ajoutent une session HITL dans le résultat.

Cette étape ne rend pas Langflow interactif.

Elle ne demande pas de validation utilisateur pendant l'exécution.

Elle prépare seulement l'exploitation future des validations humaines.
