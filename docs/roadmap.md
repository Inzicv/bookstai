# Roadmap

## Phase 1 - Fiches Markdown comme source de vérité

BookstAI ne reconstruit plus les informations à partir d'EPUB ni d'API LLM.

Workflow actuel :

- un fichier Markdown manuel existe déjà dans `memory/books/` ;
- BookstAI permet de l'importer ou de créer un template vide ;
- les fiches dans `memory/books/` sont la source de vérité.

Champs déjà présents dans les fiches :

- personnages ;
- tropes ;
- résumé ;
- citations ;
- timeline ;
- scènes importantes.

---

## Phase 2 - RAG

Recherche locale sur les fiches Markdown.

Objectif :

- retrouver rapidement les livres, citations, tropes et notes à partir d'une requête ;
- rester local et léger ;
- préparer les usages futurs de RAG sans dépendance externe.

Sources possibles :

- reviews ;
- songs ;
- humour ;
- style visuel ;
- fiches `memory/books/`.

---

## Phase 3 - Comedy Room

Proposer :

- hooks ;
- analogies ;
- références actuelles ;
- blagues ;
- punchlines.

Validation humaine.

---

## Phase 4 - Song Writer

À partir d'un résumé proposer :

- rimes ;
- idées.

Validation humaine.

---

## Phase 5 - Art Director

Prompts images.

Storyboard.

Direction artistique.

---

## Phase 6 - Animator

Prompts vidéo.

Animations.

---

## Phase 7 - Social Media

Descriptions.

Hashtags.

Carrousels.
