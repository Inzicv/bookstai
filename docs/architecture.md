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

## HITL dans la CLI

La CLI expose l'option `--hitl`.

Sans cette option, les workflows utilisent leur comportement historique.

Avec `--hitl`, la CLI appelle `run_with_hitl(...)` et ajoute une session HITL dans le résultat.

La CLI ne devient pas interactive dans cette étape.

## Contenu validé HITL

Chaque étape HITL conserve toujours le contenu original généré par l'IA.

La version réellement exploitable est exposée via `validated_content`.

Règles :

- `pending` utilise encore le contenu original ;
- `approved` utilise le contenu original ;
- `edited` utilise le contenu corrigé par l'utilisateur ;
- `rejected` retourne `None`.

`validated_content` est une valeur calculée.

La source de vérité reste :

- `status` ;
- `content` ;
- `edited_content`.

Cette logique prépare la Learning Loop et l'enrichissement futur de la mémoire.

## Learning Loop - extraction

La Learning Loop commence par une extraction depuis une session HITL.

Seules les étapes explicitement validées par l'utilisateur sont exploitables :

- `approved`
- `edited`

Les étapes `pending` sont ignorées car elles n'ont pas encore été validées.

Les étapes `rejected` sont conservées comme information, mais ne deviennent pas des candidates d'apprentissage.

Cette étape ne modifie pas encore la mémoire.

Elle prépare seulement une structure exploitable pour générer ensuite un brouillon de mise à jour mémoire.

## Learning Draft

BookstAI ne modifie pas directement la mémoire depuis une session HITL.

La Learning Loop génère d'abord un brouillon Markdown dans :

```text
outputs/learning/
```

Ce brouillon contient :

- les étapes validées ;
- les étapes éditées ;
- les contenus originaux ;
- les contenus validés ;
- les commentaires ;
- les étapes rejetées ;
- les étapes en attente.

Le brouillon doit être relu avant application.

## Persistance HITL

Les sessions HITL peuvent être sauvegardées en JSON.

Le stockage par défaut est :

```text
outputs/hitl/
```

Une session est stockée par workflow et par livre :

```text
outputs/hitl/<workflow_name>/<item_slug>.json
```

Le JSON conserve :

- le nom du workflow ;
- le slug du livre ;
- les étapes HITL ;
- le statut de chaque étape ;
- le contenu original ;
- le contenu édité si disponible ;
- les commentaires éventuels ;
- les métadonnées.

Cette persistance prépare les futures commandes de validation et d’édition.

## Commandes CLI HITL

La CLI permet de manipuler une session HITL sauvegardée.

Commandes disponibles :

```text
bookstai hitl show
bookstai hitl approve
bookstai hitl reject
bookstai hitl edit
```

Ces commandes ne relancent pas les workflows.

Elles modifient uniquement le fichier JSON de session HITL.

Elles permettent de reprendre une génération, d’approuver des étapes, de rejeter des propositions ou d’enregistrer une version corrigée.

## CLI Learning Loop

La CLI expose une commande `learning`.

Commandes disponibles :

```text
bookstai learning extract
bookstai learning draft
bookstai learning apply
```

`learning extract` lit une session HITL et extrait les candidates d'apprentissage.

`learning draft` génère un brouillon Markdown dans `outputs/learning`.

`learning apply` applique explicitement un draft dans `memory/` avec sauvegarde.

La Learning Loop ne modifie jamais la mémoire automatiquement.

L'application dans `memory/` nécessite une commande explicite.
