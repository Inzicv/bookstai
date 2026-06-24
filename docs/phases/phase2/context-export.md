# Phase 2 — export de contexte

Objectif :

Charger une seule fiche `memory/books/<slug>.md`, extraire ses sections et produire un contexte propre, prêt à être transmis à un assistant spécialisé.

Entrée :

- un fichier Markdown de livre.

Sortie :

- un objet de contexte en mémoire ;
- ou un export texte structuré ;
- ou un affichage CLI prêt à copier-coller.

Structure du contexte :

- titre ;
- chemin du fichier ;
- sections reconnues ;
- contenu textuel de chaque section.

Usage prévu :

- Review Assistant ;
- Song Assistant ;
- Comedy Room ;
- Art Director.

Contraintes :

- une seule fiche active à la fois ;
- pas de recherche multi-livres ;
- pas de RAG complexe ;
- conserver le découpage Markdown existant ;
- rester local et simple.
