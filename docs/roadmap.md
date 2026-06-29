# BookstAI Roadmap

> Version : 1.0
>
> Objectif :
>
> Construire progressivement BookstAI jusqu'à obtenir un studio personnel de création de contenu assisté par IA, basé sur des workflows agentiques, avec Human In The Loop à chaque étape.

---

# Définition de "Terminé"

BookstAI sera considéré comme terminé lorsque :

- une fiche lecture suffira à lancer un workflow complet ;
- chaque workflow sera orchestré automatiquement ;
- chaque étape pourra être validée ou modifiée par l'utilisateur ;
- la mémoire sera utilisée automatiquement ;
- les corrections pourront enrichir la mémoire après validation ;
- l'ajout d'un nouveau workflow nécessitera très peu de développement.

---

# Milestone 1 — Fondations

Objectif

Créer une base solide qui ne devra quasiment plus changer.

## À faire

- [ ] Finaliser la Vision
- [ ] Finaliser l'Architecture
- [ ] Finaliser les Workflows
- [ ] Finaliser les Agents
- [ ] Définir tous les formats d'entrée/sortie
- [ ] Définir les conventions de nommage
- [ ] Définir l'organisation des dossiers

Livrables

- docs/
- memory/
- prompts/

Critère de validation

Toute personne lisant uniquement la documentation doit comprendre comment fonctionne BookstAI.

---

# Milestone 2 — Langflow

Objectif

Construire l'orchestrateur visuel.

## À faire

- [ ] Installer Langflow
- [ ] Comprendre les Components
- [ ] Comprendre les Flows
- [ ] Comprendre les Tools
- [ ] Comprendre les Memory
- [ ] Comprendre les MCP
- [ ] Comprendre les API Keys
- [ ] Comprendre les Variables

Puis construire un premier Flow minimal.

Entrée

Livre

↓

Sortie

Hello World

Critère

Comprendre parfaitement Langflow avant d'ajouter de la logique métier.

---

# Milestone 3 — Premier Agent

Objectif

Créer le Context Builder.

Entrées

- workflow
- fiche lecture

Sortie

Contexte propre

Critère

Le Context Builder fonctionne de manière totalement indépendante.

---

# Milestone 4 — Premier Workflow

Objectif

Créer une Review complète.

Flow

Context Builder

↓

Style Memory

↓

Comedy Room

↓

Validation

↓

Review Writer

↓

Validation

↓

Social Media

↓

Validation

↓

Sortie

Critère

Produire une review complète sans intervention technique.

---

# Milestone 5 — Chanson

Objectif

Automatiser les chansons.

Flow

Context

↓

Style

↓

Comedy

↓

Song Writer

↓

Validation

↓

Prompt musique

↓

Sortie

Critère

Obtenir une chanson prête pour Suno.

---

# Milestone 6 — Mémoire

Objectif

Utiliser automatiquement la mémoire.

À faire

- charger les fichiers utiles
- limiter le contexte
- éviter les doublons
- gérer les spoilers

Critère

Chaque agent reçoit uniquement les informations dont il a besoin.

---

# Milestone 7 — Learning Loop

Objectif

Faire apprendre BookstAI.

Workflow

Version IA

↓

Version corrigée

↓

Analyse

↓

Diff

↓

Suggestion

↓

Validation

↓

Mémoire

Critère

Aucune mémoire n'est modifiée automatiquement.

---

# Milestone 8 — Industrialisation

Objectif

Transformer le prototype en véritable outil.

À faire

- historique
- logs
- gestion des erreurs
- templates
- export markdown
- export json

Critère

BookstAI peut être utilisé tous les jours.

---

# Milestone 9 — Nouveaux workflows

Créer progressivement

- Review
- Chanson
- Comedy Room
- Social Media

Puis les futurs workflows.

Tous doivent respecter la même architecture.

---

# Milestone 10 — Version 1.0

Critères

✓ Tous les workflows fonctionnent

✓ Tous les agents sont indépendants

✓ Human In The Loop partout

✓ Documentation complète

✓ Architecture stable

✓ Facile à maintenir

✓ Facile à faire évoluer

✓ Agréable à utiliser
