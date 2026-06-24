# Architecture

EPUB
↓
Librarian V1
↓
memory/books

Human In The Loop entre chaque étape.

Chaque module doit être indépendant.

Pour Librarian V1 :

- script CLI local ;
- saisie manuelle ou collage de texte ;
- génération Markdown simple ;
- pas d'appel automatique à une API externe.

Les données sont stockées principalement en Markdown.

Technologies :

- Python standard ;
- Markdown ;
- SQLite plus tard si nécessaire ;
- LangGraph et IA seulement pour les phases futures.
