# Local Image Backend

## Objectif

BookstAI génère les images via un backend local interchangeable.

OpenAI n’est pas utilisé pour générer les images.

Le backend image local doit implémenter l’interface existante `ImageBackend`.

## Interface existante

```python
class ImageBackend(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

Le workflow ne doit connaître que cette interface.

## Backend actuel

Pendant les tests et le développement, BookstAI utilise :

`MockImageBackend`

Ce backend retourne un chemin d’image fictif et ne génère aucune image réelle.

## Backend local cible

Le premier backend local cible est :

`ComfyUI`

ComfyUI sera utilisé via son API locale.

### Pourquoi ComfyUI

- fonctionne localement ;
- compatible avec une RTX 4070 Super ;
- permet d’utiliser différents modèles ;
- permet d’automatiser des workflows image ;
- ne dépend pas d’OpenAI ;
- peut rester derrière l’interface `ImageBackend`.

## Principe d’architecture

BookstAI ne doit pas dépendre directement de ComfyUI dans les workflows.

Le futur backend sera isolé dans une classe dédiée, par exemple :

`ComfyUIImageBackend`

Cette classe implémentera :

```python
generate(prompt: str) -> str
```

Et retournera le chemin de l’image générée.

## Ce que le backend devra faire

Le backend ComfyUI devra :

- recevoir un prompt validé ;
- appeler l’API locale ComfyUI ;
- attendre ou récupérer le résultat ;
- sauvegarder l’image dans un dossier de sortie ;
- retourner le chemin local de l’image générée.

## Ce que le backend ne devra pas faire

Le backend image ne devra jamais :

- écrire une review ;
- écrire une chanson ;
- modifier un prompt ;
- choisir une direction artistique ;
- modifier la mémoire ;
- appeler OpenAI ;
- appeler un LLM texte ;
- gérer le Human In The Loop.

## Configuration prévue

Paramètres probables :

- `comfyui_url`
- `workflow_path`
- `output_dir`
- `timeout`
- `poll_interval`

Ces paramètres seront ajoutés progressivement.

## Environnement cible

Machine locale :

- GPU : RTX 4070 Super
- Backend image : ComfyUI ou équivalent
- Exécution : locale
- API : locale

## Sécurité

Le backend image local ne doit pas exposer de clé API.

Il ne doit pas envoyer les prompts vers un service externe.

Il doit rester local par défaut.

## Tests

Les tests ne devront pas lancer ComfyUI.

Les tests utiliseront :

- `MockImageBackend`
- ou un faux client HTTP local
- ou un mock de transport

Aucun test ne devra générer une vraie image.

## Roadmap

### Epic 4.1 — Documentation backend image local

Définir le choix et les règles.

### Epic 4.2 — Créer un squelette ComfyUIImageBackend

Créer la classe sans dépendance lourde et avec appels mockables.

### Epic 4.3 — Tester le backend avec faux client HTTP

Valider les appels sans serveur ComfyUI réel.

### Epic 4.4 — Ajouter une factory image backend

Permettre de choisir :

- `mock`
- `comfyui`

### Epic 4.5 — Brancher le backend image dans la CLI

Permettre d’utiliser ComfyUI depuis la CLI.

### Epic 4.6 — Brancher le backend image dans Langflow

Permettre d’utiliser ComfyUI depuis les composants Langflow.

## Principe BookstAI

Le backend image local est interchangeable.

Les workflows restent stables.

Les agents restent spécialisés.

La génération image reste séparée de la génération texte.

## Squelette ComfyUIImageBackend

Le backend `ComfyUIImageBackend` existe comme première implémentation locale derrière l’interface `ImageBackend`.

Dans cette première version :

- il n’est pas branché automatiquement ;
- il n’est pas utilisé par la CLI ;
- il n’est pas utilisé par Langflow ;
- il ne nécessite pas de serveur ComfyUI pendant les tests ;
- les appels HTTP sont isolés et mockables ;
- le payload ComfyUI reste minimal et pourra évoluer.

L’objectif est de poser une base testable avant l’intégration réelle avec un workflow ComfyUI complet.

## Client HTTP ComfyUI

`ComfyUIImageBackend` dispose maintenant d’un client HTTP minimal :

`ComfyUIHTTPClient`

Ce client :

- utilise la librairie standard Python ;
- envoie des requêtes JSON ;
- reste remplaçable par un faux client dans les tests ;
- ne nécessite pas de serveur ComfyUI pendant les tests ;
- ne génère aucune image directement.

Dans cette étape, le backend prépare l’appel à l’API ComfyUI mais ne gère pas encore le cycle complet :

- `/prompt`
- `prompt_id`
- `/history`
- récupération du fichier image final

Ce cycle sera ajouté dans une étape suivante.
