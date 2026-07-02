# BookstAI local app

BookstAI expose une API FastAPI locale et une UI Next.js locale pour piloter les workflows Review, Song, Image et Social.

## Lancement local

Terminal 1:

```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

Terminal 2:

```bash
cd ui
npm install
npm run dev
```

Ouvrir:

```text
http://localhost:3000
```

## Configuration frontend

Créer ou ajuster `ui/.env.local` avec:

```env
NEXT_PUBLIC_BOOKSTAI_API_URL=http://127.0.0.1:8000
```

Le fichier `ui/.env.example` contient la même valeur par défaut.

## Comportement attendu

- mode local uniquement;
- `mock` comme provider par défaut;
- le workflow Song ne génère pas d'image;
- le workflow Song produit contexte, comedy, chanson, storyboard, prompts et social;
- le workflow Image repart des paroles d'une chanson et d'un style visuel sélectionné depuis `memory/visual_style/Prompts_visuels/`;
- le workflow Image produit style validé, storyboard et prompts finaux avec HITL;
- pas d'appel OpenAI par défaut;
- aucune clé API côté frontend;
- aucune écriture automatique dans `memory/`;
- les sessions HITL et les brouillons Learning sont stockés sous `outputs/`.
