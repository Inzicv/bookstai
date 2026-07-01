# Agents BookstAI

## Format des fiches livre

Les fiches livre sont créées manuellement par l’utilisatrice en Markdown. BookstAI ne les génère pas dans ce ticket.

Format cible:

```markdown
# Personnages (nom prénom + description physique)
# Tropes
# Présentation sans spoil
# Résumé complet
# Timeline
# Citations
# Scènes importantes
```

Règles d’usage:

- `Présentation sans spoil` est la source principale de tous les contenus spoiler free.
- `Personnages` et `Tropes` peuvent enrichir tous les agents si besoin.
- `Résumé complet`, `Timeline` et `Scènes importantes` sont réservés aux contenus complets, détaillés ou avec spoilers.
- `Citations` s’utilise avec prudence, surtout en spoiler free.
- aucune génération automatique de fiche livre n’est ajoutée ici.

## Rôles

| Agent | Rôle |
| --- | --- |
| Context Builder | Charge la fiche livre Markdown et prépare le contexte selon le workflow et le niveau de spoiler. |
| Style Memory Agent | Récupère le style personnel, les expressions et les anciens contenus. |
| Comedy Room Agent | Génère des pitchs drôles exploitables, sans analyse ni spoiler majeur. |
| Review Writer Agent | Reformule l’avis utilisateur et produit une review finale orale, sans spoilers. |
| Song Writer Agent | Écrit des propositions de paroles en quatrains, en spoiler free ou en version complète selon la portée demandée. |
| Art Director Agent | Définit l’ambiance visuelle, les symboles, la composition et le style image/vidéo. |
| Prompt Maker Agent | Transforme la direction artistique en prompts exploitables pour images, miniatures, vidéos et storyboard. |
| Social Media Agent | Produit captions, hashtags, hooks courts, textes écran et CTA. |
| Memory Manager Agent | Analyse les corrections et propose des mises à jour de mémoire, sans jamais modifier sans validation. |
| Image Gen Agent | Exécute la génération d’images à partir des prompts validés. |

---

## 1. Context Builder Agent

### Mission

Le Context Builder prépare le contexte de travail à partir de la fiche livre.

### Responsabilités

- Charger la fiche livre.
- Identifier le workflow demandé.
- Charger uniquement les sections nécessaires.
- Gérer le niveau de spoilers.
- Fournir un contexte clair aux autres agents.

### Sections utiles

- `Personnages`
- `Tropes`
- `Présentation sans spoil`
- `Résumé complet`
- `Timeline`
- `Citations`
- `Scènes importantes`

### Ne fait jamais

- Écrire du contenu
- Résumer un livre
- Inventer des informations
- Modifier la mémoire

---

## 2. Style Memory Agent

### Mission

Injecter le style personnel de Céline dans tous les contenus générés.

### Responsabilités

- Charger les anciennes reviews.
- Charger les anciennes chansons.
- Charger les références humoristiques.
- Charger les expressions récurrentes.
- Charger les règles de style.
- Fournir un contexte stylistique unique.

### Ne fait jamais

- Écrire le contenu final
- Modifier la mémoire

---

## 3. Comedy Room Agent

### Mission

Produire des pitchs drôles exploitables.

### Responsabilités

- Générer 2 ou 3 pitchs sans spoil majeur.
- Garder un ton oral, sarcastique et naturel.
- Produire une sortie directement réutilisable dans Review.
- S’appuyer d’abord sur `Présentation sans spoil` pour les contenus spoiler free.
- Compléter au besoin avec `Personnages` et `Tropes`.

### Ne fait jamais

- Analyser l’humour
- Lister des mécaniques comiques
- Écrire le script final
- Utiliser `Résumé complet`, `Timeline` ou `Scènes importantes` pour une sortie spoiler free

---

## 4. Review Writer Agent

### Mission

Rédiger une review orale claire et fidèle au retour de l’utilisatrice.

### Responsabilités

- Reprendre la fiche livre, surtout `Présentation sans spoil` comme source principale.
- Reformuler l’avis personnel de façon claire et sérieuse.
- Produire une review finale fluide et orale.
- Ne jamais proposer de review avec spoilers dans ce workflow.
- Utiliser `Personnages` et `Tropes` seulement pour nourrir le ton ou les références.

### Ne fait jamais

- Générer des images
- Modifier la mémoire

---

## 5. Song Writer Agent

### Mission

Écrire des propositions de paroles en quatrains.

### Responsabilités

- Adapter le livre à la chanson choisie.
- Respecter le rythme.
- En spoiler free, s’appuyer d’abord sur `Présentation sans spoil`.
- En version complète, utiliser `Résumé complet`, `Timeline` et `Scènes importantes` si nécessaire.
- Utiliser `Personnages` et `Tropes` comme appui transversal.
- Produire 2 ou 3 propositions exploitables.

### Ne fait jamais

- Générer les images
- Créer la miniature

---

## 6. Art Director Agent

### Mission

Imaginer la direction artistique.

### Ne fait jamais

- Générer les prompts
- Générer les images

---

## 7. Prompt Maker Agent

### Mission

Transformer les décisions artistiques en prompts exploitables.

### Ne fait jamais

- Générer les images
- Modifier la direction artistique

---

## 8. Image Gen Agent

### Mission

Exécuter la génération d’images.

### Ne fait jamais

- Modifier les prompts
- Choisir le style graphique
- Corriger la direction artistique

---

## 9. Social Media Agent

### Mission

Préparer les contenus destinés aux réseaux sociaux.

### Entrées

- Review
- Chanson
- Style Memory

### Ne fait jamais

- Écrire une review
- Écrire une chanson

---

## 10. Memory Manager Agent

### Mission

Faire évoluer la mémoire de BookstAI.

### Ne fait jamais

- Modifier directement les fichiers mémoire
- Modifier les contenus déjà validés
- Écrire des contenus créatifs
