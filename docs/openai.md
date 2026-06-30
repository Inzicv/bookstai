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

## Factory LLM

BookstAI fournit une factory simple pour créer un client LLM selon le provider demandé.

```python
from bookstai.llm import create_llm_client

client = create_llm_client(
    provider="mock",
)
```

Pour OpenAI :

```python
from bookstai.llm import create_llm_client

client = create_llm_client(
    provider="openai",
    model="gpt-4o-mini",
    temperature=0.7,
)
```

La factory ne branche pas encore OpenAI automatiquement dans les workflows.
Elle sert uniquement à centraliser la création du client LLM.

Providers supportés actuellement :

- `mock`
- `openai`

Providers connus mais non supportés dans cette factory :

- `anthropic`
- `ollama`

## Utilisation via Langflow

Les composants Langflow BookstAI peuvent utiliser OpenAI via le champ `provider`.

Par défaut, ils utilisent `mock`.

Pour activer OpenAI :

- `provider` : `openai`
- `model` : `gpt-4o-mini`
- `temperature` : `0.7`

La variable `OPENAI_API_KEY` doit être définie dans l’environnement qui exécute Langflow.

La clé API ne doit pas être saisie directement dans le flow.

OpenAI reste optionnel et désactivé par défaut.
