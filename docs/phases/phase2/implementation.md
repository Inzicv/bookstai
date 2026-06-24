# Phase 2 — implementation

But technique :

Fournir une mémoire locale créative pour les assistants futurs, sans transformer le projet en moteur de recherche généraliste.

Principe :

- les fiches Markdown restent la source de vérité ;
- on indexe leur contenu par sections ;
- on récupère des fragments de contexte pertinents ;
- on n’écrit jamais dans les fiches pour reconstruire des données.

Architecture minimale :

1. Ingestion
   - lire `memory/books/*.md`
   - détecter les titres de section
   - découper en fragments

2. Index local
   - base SQLite légère
   - un enregistrement par fragment
   - métadonnées : titre, section, chemin, ordre

3. Récupération
   - recherche textuelle simple
   - classement de pertinence
   - renvoi de fragments de contexte

4. Sortie
   - affichage des sections pertinentes
   - prêt pour réutilisation par les futures phases créatives

Points de vigilance :

- ne pas modifier `docs/roadmap.md` ;
- ne pas modifier `docs/workflows.md` ;
- ne pas déduire de nouvelles règles fonctionnelles ;
- conserver l’existant utile ;
- privilégier Python standard.
