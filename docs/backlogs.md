# BookstAI Product Backlog

---

# EPIC 1 — Architecture

Objectif

Poser les fondations du projet.

## Features

### ARCH-001 Documentation

- [ ] Vision
- [ ] Architecture
- [ ] Agents
- [ ] Workflows
- [ ] Roadmap
- [ ] Backlog

Critère

Toute personne comprend le fonctionnement du projet.

---

### ARCH-002 Arborescence

- [ ] docs/
- [ ] memory/
- [ ] prompts/
- [ ] outputs/
- [ ] flows/

Critère

La structure ne changera plus.

---

# EPIC 2 — Langflow

Objectif

Construire le studio visuel.

## FLOW-001

Créer le Flow principal.

Critères

- sélection workflow
- lancement
- validation

---

## FLOW-002

Créer les Components personnalisés.

- Context Builder
- Style Loader
- Comedy
- Writer
- Social

---

## FLOW-003

Variables globales

- modèle
- température
- fournisseur
- dossier mémoire

---

# EPIC 3 — Mémoire

## MEM-001

Chargement des livres

Entrée

Livre.md

Sortie

Contexte

---

## MEM-002

Style

Charger

- reviews
- humour
- chansons

---

## MEM-003

Spoilers

Permettre

- aucun
- léger
- complet

---

# EPIC 4 — Review

Objectif

Workflow complet.

## REV-001

Context Builder

Entrées

- livre
- workflow

Sortie

Contexte

---

## REV-002

Comedy Room

Produit

- hooks
- comparaisons
- punchlines

---

## REV-003

Review Writer

Produit

Review finale

---

## REV-004

Validation

Accepter

Modifier

Rejeter

---

## REV-005

Social

Produit

- description
- hashtags
- CTA

---

# EPIC 5 — Chanson

SON-001

Version spoiler free

---

SON-002

Version complète

---

SON-003

Prompt Suno

---

SON-004

Validation

---

# EPIC 6 — Learning

LEARN-001

Comparer

IA

↓

Version corrigée

---

LEARN-002

Calculer le diff

---

LEARN-003

Détecter

- nouveaux tics
- nouvelles expressions
- nouvelles règles

---

LEARN-004

Proposer

une mise à jour mémoire

---

# EPIC 7 — Historique

HIST-001

Sauvegarder

- prompt
- réponse
- corrections

---

HIST-002

Pouvoir rejouer une génération

---

# EPIC 8 — Export

EXP-001

Markdown

---

EXP-002

JSON

---

EXP-003

Copie presse-papier

---

# EPIC 9 — Version 1

Critères

✓ Tous les workflows fonctionnent

✓ Tous les agents sont documentés

✓ Langflow orchestre tout

✓ Human In The Loop

✓ La mémoire fonctionne

✓ Les corrections enrichissent la mémoire

✓ Documentation terminée

✓ Projet facilement extensible
