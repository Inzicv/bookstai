# Roadmap

# Phase 1 - Base de connaissances
Les fichiers Markdown sont la source de vérité.
Sources :
* memory/books/
* memory/reviews/
* memory/songs/
* memory/humor/
* memory/visual_style/
Les fiches livres sont créées manuellement (ChatGPT ou utilisateur).
BookstAI ne lit pas automatiquement les EPUB.
Objectif :
Constituer une mémoire de qualité.
✅ Terminé

# Phase 2 - RAG créatif local
Construire une mémoire créative locale légère.
Sources :
* memory/books/
* memory/reviews/
* memory/songs/
* memory/humor/
* memory/visual_style/
Objectif :
Transformer une requête naturelle en contexte exploitable.
Exemples :
"Je veux une review humoristique sur Les Héritiers d'Orion"
"Je veux une parodie spoiler-free sur Crescent City"
Le système doit fournir :
* résumé ;
* personnages ;
* tropes ;
* citations ;
* scènes importantes ;
* exemples de reviews similaires ;
* exemples de chansons similaires ;
* références humoristiques ;
* références visuelles.
Il ne s'agit pas d'un moteur de recherche mais d'une mémoire créative.
🚧 Phase actuelle

# Phase 3 - Comedy Room
Premier assistant créatif.
Entrée :
Contexte produit par le RAG.
Sortie :
* résumé humoristique / pitch de livre tel que dans le contexte
- hooks ;
- analogies ;
- références actuelles ;
- blagues ;
- punchlines.
L'utilisateur garde toujours la décision finale.

# Phase 4 - Song Writer
Assistant de co-écriture.
Entrée :
Contexte produit par le RAG.
Sortie :
* idées ;
* structures ;
* rimes ;
* scènes importantes ;
* propositions de paroles de chanson (2 à 3 exemples).
-
L'utilisateur conserve l'écriture finale.

# Phase 5 - Art Director
Assistant de direction artistique.
Entrée :
Contexte produit par le RAG.
Sources :
* memory/books
* memory/visual_style
Sortie :
* prompts images ;
* idées de storyboard ;
* cadrages ;
* plans ;
* références visuelles.
Le style n'est jamais imposé.

# Phase 6 - Assistant de création visuelle
Assistant de création visuelle basé sur ce qui a été produit dans Song Writer.
Sortie :
* prompts image ;
* prompts vidéo ;
* mouvements ;
* expressions ;
* idées d'animation.

# Phase 7 - Social Media
Assistant publication.
Sortie :
* descriptions ;
* hashtags ;
* hooks ;
* carrousels ;
* légendes optimisées Bookstagram ;
* légendes optimisées BookTok.

# Principes
Toujours privilégier :
* simplicité ;
* faible coût ;
* local ;
* Markdown ;
* Human In The Loop.
Éviter :
* lecture automatique des romans ;
* agents autonomes ;
* pipelines coûteux ;
* complexité inutile.