# Phase 3 — Review Assistant

## Objectif

Aider à construire une review humoristique fidèle au style de l'utilisatrice sans remplacer sa créativité.

Une review contient :

1. Hook
2. Pitch humoristique du livre
3. Avis personnel

L'utilisateur reste auteur du script final.

## Sources utilisées

### Livre actif

`memory/books/<slug>.md`

Utilisé pour :

- le résumé ;
- les personnages ;
- les tropes ;
- les scènes importantes.

### Reviews précédentes

`memory/reviews/reviews.md`

Les anciennes reviews servent de références de ton, de structure et d'humour.

### Références humoristiques

`memory/humor/references.md`

Contient :

- artistes ;
- humoristes ;
- créateurs ;
- références ;
- style d'humour.

## Étape 1 : construction du pitch

À partir du résumé du livre, le Review Assistant prépare :

- un résumé humoristique ;
- plusieurs idées ;
- des analogies ;
- des références ;
- des métaphores ;
- des blagues potentielles.

L'objectif n'est pas d'écrire le pitch final, mais d'aider l'utilisateur à le construire.

## Étape 2 : construction de l'avis

Une fois le pitch validé, l'utilisateur donne son avis brut.

Le Review Assistant :

- remet les idées dans l'ordre ;
- améliore la formulation ;
- conserve le ton habituel ;
- s'appuie sur les anciens avis.

## Étape 3 : propositions de hooks

Une fois le pitch et l'avis validés, le Review Assistant propose 2 ou 3 hooks possibles.

## Étape 4 : script final

Le Review Assistant assemble :

- hook validé ;
- pitch validé ;
- avis validé.

Il produit un script propre.

## Principes

Human In The Loop partout.

Le Review Assistant ne remplace jamais l'humour ou la créativité.

Il propose.

L'utilisateur décide.
