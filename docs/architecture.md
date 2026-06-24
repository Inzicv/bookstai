# Architecture

Source de vérité :

`memory/books/*.md`

Flux principal :

Markdown manuel
↓
BookstAI
↓
Import ou template
↓
`memory/books/<slug>.md`

Principes :

- pas d'analyse automatique d'EPUB ;
- pas d'appel LLM obligatoire ;
- architecture simple ;
- Python standard en priorité ;
- réutiliser les fiches existantes.

Human In The Loop partout.

Chaque module doit rester indépendant.
