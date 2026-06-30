# Usage quotidien BookstAI

## Cycle Review

1. Générer une review avec HITL.
2. Relire la session HITL.
3. Éditer ou approuver les étapes.
4. Générer un Learning Draft.
5. Appliquer le draft dans la mémoire si pertinent.
6. Consulter l’historique.

## Cycle Song

1. Générer une chanson avec HITL.
2. Relire les étapes.
3. Corriger la chanson ou la légende.
4. Générer un Learning Draft.
5. Appliquer le draft si pertinent.

## Règle importante

BookstAI ne modifie jamais la mémoire automatiquement.

La mémoire est modifiée uniquement via :

```text
bookstai learning apply
```

## Historique

Chaque commande importante écrit une entrée dans :

```text
outputs/history/bookstai-history.jsonl
```

## Debug

Utiliser :

```text
--verbose
```

pour afficher plus d’informations.
