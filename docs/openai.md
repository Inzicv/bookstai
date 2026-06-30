# OpenAI Integration

## Objectif

OpenAI est utilisé uniquement pour les tâches de génération de texte.

## Statut

Le client OpenAI réel existe, mais il n’est pas encore branché automatiquement dans les workflows.

## Installation

```bash
pip install -e ".[openai]"
```

## Configuration

Définir la variable d’environnement :

```bash
OPENAI_API_KEY=...
```

## Utilisation directe

```python
from bookstai.llm import OpenAILLMClient

client = OpenAILLMClient(
    model="gpt-4o-mini",
    temperature=0.7,
)

response = client.generate("Écris une review courte.")
```

## Limites

- pas encore utilisé par la CLI ;
- pas encore utilisé par Langflow ;
- pas encore de suivi de coût ;
- pas encore de retry avancé ;
- pas de génération d’image avec OpenAI.
