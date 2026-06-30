# OpenAI Integration

## Objectif

OpenAI est utilisé uniquement pour les tâches de génération de texte.

Il peut être utilisé par :

- le client direct `OpenAILLMClient` ;
- la factory `create_llm_client` ;
- la CLI BookstAI ;
- les composants Langflow BookstAI.

OpenAI n’est jamais utilisé pour la génération d’images.

## Statut

OpenAI est intégré comme provider texte optionnel.

Par défaut, BookstAI utilise toujours le provider `mock`.

Aucun appel OpenAI n’est effectué tant que `provider` n’est pas explicitement défini à `openai`.

## Installation

```bash
pip install -e ".[openai]"
```

## Configuration

Définir la variable d’environnement :

```bash
OPENAI_API_KEY=...
```

La clé API ne doit jamais être :

- écrite dans le code ;
- saisie dans Langflow ;
- stockée dans un fichier mémoire ;
- commitée dans Git ;
- affichée dans une erreur ;
- loggée.

Elle est lue uniquement par `OpenAILLMClient`.

## Utilisation directe

```python
from bookstai.llm import OpenAILLMClient

client = OpenAILLMClient(
    model="gpt-4o-mini",
    temperature=0.7,
)

response = client.generate("Écris une review courte.")
```

## Factory LLM

```python
from bookstai.llm import create_llm_client

client = create_llm_client(
    provider="openai",
    model="gpt-4o-mini",
    temperature=0.7,
)
```

Providers supportés actuellement :

- `mock`
- `openai`

Providers connus mais non supportés dans cette factory :

- `anthropic`
- `ollama`

## Utilisation via la CLI

Par défaut, la CLI utilise `mock`.

Review avec mock :

```bash
bookstai review \
  --book example \
  --opinion "J'ai aimé l'ambiance." \
  --platform tiktok
```

Review avec OpenAI :

```bash
bookstai review \
  --book example \
  --opinion "J'ai aimé l'ambiance." \
  --platform tiktok \
  --provider openai \
  --model gpt-4o-mini \
  --temperature 0.7
```

Song avec mock :

```bash
bookstai song \
  --book example \
  --spoiler-mode spoiler_free \
  --prompt-type thumbnail \
  --platform tiktok
```

Song avec OpenAI :

```bash
bookstai song \
  --book example \
  --spoiler-mode spoiler_free \
  --prompt-type thumbnail \
  --platform tiktok \
  --provider openai \
  --model gpt-4o-mini \
  --temperature 0.7
```

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

## Sécurité

Règles obligatoires :

- ne jamais committer une clé API ;
- ne jamais mettre une clé API dans `memory/` ;
- ne jamais mettre une clé API dans `prompts/` ;
- ne jamais mettre une clé API dans un export ;
- ne jamais afficher une clé API dans une exception ;
- ne jamais stocker la clé API dans un attribut public ;
- garder `mock` comme provider par défaut.

## Coûts

OpenAI est facturé à l’usage.

Pour éviter les dépenses involontaires :

- garder `provider=mock` pendant les tests ;
- utiliser OpenAI seulement sur les générations utiles ;
- ne pas lancer les workflows en boucle ;
- éviter les appels automatiques non validés ;
- préférer les mocks pendant le développement ;
- réserver OpenAI aux contenus réellement créatifs ou proches de la publication.

## Limites actuelles

- pas de suivi automatique des coûts ;
- pas de budget maximum intégré ;
- pas de retry avancé ;
- pas de streaming ;
- pas de LLM local texte ;
- pas de génération d’image avec OpenAI.

## Principe BookstAI

OpenAI est un moteur texte interchangeable.

Les workflows ne dépendent pas directement d’OpenAI.

Ils reçoivent uniquement un client compatible `LLMClient`.
