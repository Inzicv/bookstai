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

Options image:

- `--image-backend` avec `mock` par défaut
- `--image-path` avec `outputs/mock/image.png` par défaut
- `--comfyui-url` avec `http://127.0.0.1:8188` par défaut
- `--comfyui-workflow-path` avec `None` par défaut
- `--image-output-dir` avec `outputs/images` par défaut
- `--image-timeout` avec `60.0` par défaut
- `--image-poll-interval` avec `1.0` par défaut

Exemple offline par défaut:

```bash
bookstai song --book alchemised --story-scope pitch_only --song-style parody --platform instagram
```

Exemple explicite avec ComfyUI:

```bash
bookstai song --book alchemised --story-scope pitch_only --song-style parody --platform instagram
```
