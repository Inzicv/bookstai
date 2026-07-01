# Workflows BookstAI

## Review

Objectif: produire une review humoristique fidèle au style de référence.

Workflow:

```text
Livre
↓
Context Builder Agent
↓
Style Memory Agent
↓
Comedy Room Agent
↓
Review Writer Agent
↓
Validation humaine
↓
Social Media Agent
```

Sortie:

- context
- style
- comedy
- review
- social

Session HITL:

- comedy
- review
- social

## Song

Objectif: produire une chanson parodique narrative sans génération d'image.

Workflow:

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
Art Director Agent
↓
Validation humaine
↓
Prompt Maker Agent
↓
Social Media Agent
```

Sortie:

- context
- style
- comedy
- song
- storyboard
- prompts
- social

Session HITL:

- comedy
- song
- storyboard
- prompts
- social

Song ne génère pas d'image.
Les prompts produits servent à un futur module image séparé.

## Comedy Room

Objectif: créer une banque d'humour réutilisable.

Workflow:

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
```

## Social Media

Objectif: préparer les contenus destinés aux réseaux sociaux.

Workflow:

```text
Contenu validé
↓
Style Memory Agent
↓
Social Media Agent
↓
Validation humaine
```

