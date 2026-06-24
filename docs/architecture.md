# Architecture

Source de vérité :

`memory/books/*.md`

Flux principal :

Markdown manuel
↓
BookstAI
↓
Import, template ou recherche locale
↓
`memory/books/<slug>.md`

Principes :

- pas d'analyse automatique d'EPUB ;
- pas d'appel LLM obligatoire ;
- architecture simple ;
- Python standard en priorité ;
- réutiliser les fiches existantes ;
- la recherche locale parcourt les Markdown sans reconstruire les données.

Human In The Loop partout.

Chaque module doit rester indépendant.
