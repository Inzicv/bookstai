# Agents

| Agent                    | Rôle                                                                                                                       |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| **Context Builder**      | Charge la fiche livre Markdown et prépare le bon contexte selon le workflow : review, chanson, miniature, storyboard, etc. |
| **Style Memory Agent**   | Récupère ton style, ton humour, tes expressions et tes anciens contenus.                                                   |
| **Comedy Room Agent**    | Génère hooks, punchlines, analogies, vannes, références pop culture.                                                       |
| **Review Writer Agent**  | Assemble une review humoristique avec la structure Hook → Pitch → Avis personnel, déjà définie dans ton workflow.          |
| **Song Writer Agent**    | Écrit les chansons parodiques, en version spoiler free ou version complète.                                                |
| **Art Director Agent**   | Définit l’ambiance visuelle, les symboles, la composition, le style image/vidéo.                                           |
| **Prompt Maker Agent**   | Transforme la direction artistique en prompts exploitables pour images, miniatures, vidéos, storyboard.                    |
| **Social Media Agent**   | Produit captions, hashtags, hooks courts, textes écran, CTA.                                                               |
| **Memory Manager Agent** | Analyse tes corrections et propose des mises à jour de mémoire, sans jamais modifier sans validation.                      |
| **Image Gen Agent**      | Exécuter la génération d’images à partir des prompts validés.                                                              |


# Agents BookstAI

---

# 1. Context Builder Agent

## Mission

Le Context Builder est le point d'entrée de tous les workflows BookstAI.

Son rôle est de préparer le contexte de travail à partir de la fiche livre.

Il ne crée jamais de contenu.

---

## Responsabilités

* Charger la fiche livre.
* Identifier le workflow demandé.
* Charger uniquement les sections nécessaires.
* Gérer les différents profils de contexte.
* Gérer le niveau de spoilers.
* Fournir un contexte clair aux autres agents.

---

## Entrées

### Obligatoires

* `memory/books/<livre>.md`
* Workflow demandé

### Paramètres

* Profil de contexte
* Niveau de spoiler
* Sections souhaitées

---

## Sorties

Un contexte structuré contenant uniquement les informations utiles.

---

## Utilise

* `memory/books/<livre>.md`

---

## Ne fait jamais

* Écrire du contenu
* Résumer un livre
* Inventer des informations
* Modifier la mémoire

---

# 2. Style Memory Agent

## Mission

Injecter le style personnel de Céline dans tous les contenus générés.

---

## Responsabilités

* Charger les anciennes reviews.
* Charger les anciennes chansons.
* Charger les références humoristiques.
* Charger les expressions récurrentes.
* Charger les règles de style.
* Fournir un contexte stylistique unique.

---

## Entrées

* Contexte du livre
* Workflow demandé

---

## Sorties

Un contexte stylistique.

---

## Utilise

* `memory/reviews/`
* `memory/songs/`
* `memory/humor/`

---

## Ne fait jamais

* Écrire le contenu final
* Modifier la mémoire

---

# 3. Comedy Room Agent

## Mission

Produire les idées humoristiques.

---

## Responsabilités

* Générer des hooks.
* Générer des punchlines.
* Trouver des analogies.
* Trouver des références pop culture.
* Proposer des réactions exagérées.
* Générer plusieurs variantes.

---

## Entrées

* Contexte du livre
* Style Memory

---

## Sorties

Une banque d'idées humoristiques.

---

## Utilise

* `memory/humor/`
* `memory/reviews/`

---

## Ne fait jamais

* Écrire le script final.

---

# 4. Review Writer Agent

## Mission

Rédiger une review humoristique fidèle au style de Céline.

---

## Responsabilités

* Assembler le Hook.
* Écrire le Pitch humoristique.
* Reformuler l'avis personnel.
* Produire une version finale fluide.

---

## Entrées

* Context Builder
* Style Memory
* Comedy Room
* Avis utilisateur

---

## Sorties

Le script final.

---

## Ne fait jamais

* Générer des images.
* Modifier la mémoire.

---

# 5. Song Writer Agent

## Mission

Écrire les chansons parodiques.

---

## Responsabilités

* Adapter le livre à la chanson choisie.
* Respecter le rythme.
* Produire une version spoiler free.
* Produire une version complète.
* Ajouter les indications utiles à Suno.

---

## Entrées

* Context Builder
* Style Memory
* Comedy Room

---

## Sorties

Les paroles finales.

---

## Ne fait jamais

* Générer les images.
* Créer la miniature.

---

# 6. Art Director Agent

## Mission

Imaginer toute la direction artistique.

---

## Responsabilités

* Choisir le style graphique.
* Définir l'ambiance.
* Définir la palette.
* Déterminer les objets symboliques.
* Déterminer la composition.
* Déterminer les scènes importantes.

---

## Entrées

* Context Builder
* Style Memory

---

## Sorties

Une direction artistique complète.

---

## Ne fait jamais

* Générer les prompts.
* Générer les images.

---

# 7. Prompt Maker Agent

## Mission

Transformer les décisions artistiques en prompts exploitables.

---

## Responsabilités

* Générer les prompts personnages.
* Générer les prompts scènes.
* Générer les prompts miniatures.
* Générer les prompts vidéo.
* Adapter les prompts au modèle utilisé.

---

## Entrées

* Art Director

---

## Sorties

Une collection de prompts prêts à être utilisés.

---

## Ne fait jamais

* Générer les images.
* Modifier la direction artistique.

---

# 8. Image Gen Agent

## Mission

Exécuter la génération d'images.

---

## Responsabilités

* Recevoir les prompts validés.
* Appeler le modèle de génération.
* Générer les personnages.
* Générer les scènes.
* Générer les miniatures.
* Vérifier que toutes les images ont été produites.
* Retourner les images générées.

---

## Entrées

* Prompts validés.
* Paramètres de génération.

---

## Sorties

Les images générées.

---

## Ne fait jamais

* Modifier les prompts.
* Choisir le style graphique.
* Corriger la direction artistique.

---

# 9. Social Media Agent

## Mission

Préparer les contenus destinés aux réseaux sociaux.

---

## Responsabilités

* Rédiger les descriptions.
* Générer les hashtags.
* Générer les CTA.
* Générer les hooks de publication.
* Adapter le contenu selon la plateforme.

---

## Entrées

* Review
* Chanson
* Style Memory

---

## Sorties

Le contenu prêt à publier.

---

## Ne fait jamais

* Écrire une review.
* Écrire une chanson.

---

# 10. Memory Manager Agent

## Mission

Faire évoluer la mémoire de BookstAI.

---

## Responsabilités

* Comparer les versions avant/après correction.
* Identifier les modifications récurrentes.
* Détecter les nouveaux tics d'écriture.
* Proposer des mises à jour.
* Attendre une validation humaine avant toute modification.

---

## Entrées

* Contenu généré
* Contenu corrigé

---

## Sorties

Une proposition de mise à jour de la mémoire.

---

## Ne fait jamais

* Modifier directement les fichiers mémoire.
* Modifier les contenus déjà validés.
* Écrire des contenus créatifs.

```
```
