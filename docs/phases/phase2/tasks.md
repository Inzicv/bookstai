# Phase 2 — tâches locales

Objectif interne :

Construire un RAG créatif local capable de servir de mémoire aux futurs assistants, à partir des fiches Markdown existantes.

Sous-objectifs techniques :

1. Indexer les fiches `memory/books/*.md`.
2. Découper les fiches en sections réutilisables.
3. Stocker les fragments utiles dans une base locale.
4. Retrouver rapidement les passages pertinents à partir d'une requête.
5. Afficher le contexte utile sans modifier les fichiers source.

Tâches intermédiaires :

- créer un index local ;
- parser les sections Markdown ;
- stocker les chunks dans SQLite ;
- exposer une récupération par requête ;
- afficher les sections pertinentes en sortie CLI ;
- conserver la source de vérité dans les Markdown.
