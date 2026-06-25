# BookstAI — Tuto de démarrage

Ce fichier rassemble les commandes utiles pour faire fonctionner BookstAI.

Les fichiers Markdown dans `memory/` restent la source de vérité.

## 1. Lancer le projet

Depuis la racine du projet :

```bash
python main.py
```

Cela ouvre le petit menu CLI pour :

- importer un fichier Markdown existant ;
- créer un template vide.

## 2. Importer une fiche livre existante

```bash
python main.py --source "C:\chemin\vers\mon_livre.md"
```

La fiche est copiée dans `memory/books/` avec un nom de fichier propre.

## 3. Créer un template vide

```bash
python main.py --template --title "Mon livre"
```

Si `--title` n’est pas fourni, le script le demande au lancement.

## 4. Indexer les fiches Markdown

```bash
python main.py index
```

Reconstruit l’index local des fiches dans `memory/books/`.

## 5. Faire une recherche locale

```bash
python main.py search
```

Le script demande une requête et affiche les fiches correspondantes.

Version avec requête via le titre optionnel :

```bash
python main.py search --title "enemies to lovers"
```

## 6. Voir la mémoire d’une fiche

```bash
python main.py memory
```

Affiche les résultats pertinents avec leurs sections utiles.

## 7. Préparer un brouillon de review

```bash
python main.py review --book "memory/books/lesheritiersdorion.md"
```

Avec notes brutes :

```bash
python main.py review --book "memory/books/lesheritiersdorion.md" --notes "J’ai aimé la tension et l’humour."
```

Avec export du brouillon :

```bash
python main.py review --book "memory/books/lesheritiersdorion.md" --notes "J’ai aimé la tension et l’humour." --output "review_draft.md"
```

### Scénario de test manuel complet

Si la fiche de test existe, lance :

```bash
python main.py review --book "memory/books/lesheritiersdorion.md" --run-all
```

Pour assembler sans demander la confirmation finale :

```bash
python main.py review --book "memory/books/lesheritiersdorion.md" --run-all --skip-confirm
```

Déroulé attendu :

1. proposition de pitch ;
2. saisie du pitch corrigé ;
3. saisie de l'avis brut ;
4. proposition d'avis ;
5. saisie de l'avis corrigé ;
6. propositions de hooks ;
7. choix du hook final ;
8. assemblage du script final.

## 8. Charger une fiche active et exporter son contexte

```bash
python main.py context --book "memory/books/lesheritiersdorion.md"
```

Avec export texte :

```bash
python main.py context --book "memory/books/lesheritiersdorion.md" --export "context.txt"
```

## 9. Fichiers mémoire utiles

- `memory/books/<livre>.md`
- `memory/reviews/reviews.md`
- `memory/humor/references.md`
- `memory/songs/`
- `memory/visual_style/`

## 10. Règle de travail

- une seule fiche livre active à la fois ;
- Human In The Loop partout ;
- pas de couche inutile ;
- les Markdown restent la source de vérité.
