# CLI

La CLI `bookstai` utilise maintenant les factories validées du projet.

## Commande `review`

Options LLM:

- `--provider` avec `mock` par défaut
- `--model` avec `gpt-4o-mini` par défaut
- `--temperature` avec `0.7` par défaut

Exemple offline par défaut:

```bash
bookstai review --book alchemised --opinion "J'ai adoré mais j'ai souffert." --platform instagram
```

Exemple explicite avec OpenAI:

```bash
bookstai review --book alchemised --opinion "J'ai adoré mais j'ai souffert." --platform instagram --provider openai --model gpt-4o-mini --temperature 0.7
```

## Commande `song`

Options LLM:

- `--provider` avec `mock` par défaut
- `--model` avec `gpt-4o-mini` par défaut
- `--temperature` avec `0.7` par défaut

Exemple offline par défaut:

```bash
bookstai song --book alchemised --story-scope pitch_only --song-style parody --platform instagram
```

## Workflow `image`

Le workflow Image est exposé via l’UI et l’API séparées. Il repart des paroles d’une chanson déjà validée et d’un style visuel choisi depuis `memory/visual_style/Prompts_visuels/`.
