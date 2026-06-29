# Workflows BookstAI

---

# Review humoristique

## Objectif

Produire une review humoristique fidèle au style de Céline.

## Structure

```text
Hook
↓
Pitch humoristique
↓
Avis personnel
```

## Workflow

```text
Livre
↓
Context Builder Agent
↓
Style Memory Agent
↓
Comedy Room Agent
    ↓
    Génère :
    - Hook
    - Pitch humoristique complet
    - Références pop culture
    - Idées de memes
↓
Validation humaine
↓
Avis personnel de Céline
↓
Review Writer Agent
    ↓
    Assemble :
    - Hook
    - Pitch humoristique
    - Avis personnel
↓
Review finale
↓
Validation humaine
↓
Social Media Agent
↓
Description
Hashtags
CTA
↓
Memory Manager Agent
```

---

# Chanson parodique

## Objectif

Créer une chanson parodique inspirée d'un livre.

## Paramètres

* Spoiler free
* Histoire complète

## Workflow

```text
Livre
↓
Context Builder Agent
↓
Style Memory Agent
↓
Comedy Room Agent
↓
Song Writer Agent
↓
Validation humaine
↓
Suno
↓
Art Director Agent
    ↓
    Définit :
    - style graphique
    - ambiance
    - personnages à illustrer
    - scènes importantes
↓
Validation humaine
↓
Prompt Maker Agent
    ↓
    Génère :
    - prompts personnages
    - prompts scènes
↓
Validation humaine
↓
Image Gen Agent
↓
Images générées
↓
Social Media Agent
↓
Description
Hashtags
CTA
↓
Memory Manager Agent
```

---

# Comedy Room

## Objectif

Créer une banque d'humour réutilisable.

## Workflow

```text
Livre
↓
Context Builder Agent
↓
Style Memory Agent
↓
Comedy Room Agent
↓
Validation humaine
↓
Hooks
Punchlines
Analogies
Comparaisons
Références pop culture
Idées de memes
```

---

# Social Media

## Objectif

Préparer les contenus destinés aux réseaux sociaux.

## Workflow

```text
Contenu validé
↓
Style Memory Agent
↓
Social Media Agent
↓
Validation humaine
↓
Publication
```
