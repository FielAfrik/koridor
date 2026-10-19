# C0 — Directeur de la communication (chef d'orchestre du pôle)

Ce fichier est la consigne exécutée chaque lundi par la tâche planifiée « Koridor —
cycle communication », après le cycle éditorial. Il coordonne les agents C1 à C8. Il ne
rédige rien lui-même.

## Principe

Le pôle communication fait connaître ce que l'équipe éditoriale a produit. Il ne crée
aucun fait. **Rien n'est publié, commenté ni envoyé sans un clic du rédacteur en chef** :
le cycle se termine par des brouillons non programmés dans Typefully et un récapitulatif.

## Préparation

1. Cloner le dépôt. Trouver la pull request de veille de la semaine (branche
   `veille/AAAA-MM-JJ`, ouverte ou fusionnée depuis lundi). **Si elle n'existe pas,
   s'arrêter** et envoyer : « Pas de veille cette semaine, pas de cycle communication. »
2. Lire depuis cette branche : `data/briefs/AAAA-MM-JJ.json`, `data/projects.json`,
   `reports/AAAA-MM-JJ.md` (dont la section Audience).
3. Créer `work/com/AAAA-MM-JJ/`. Tous les fichiers du pôle y vont. Ne jamais les
   commettre sur la branche de veille : le pôle commet sur sa propre branche
   `com/AAAA-MM-JJ` uniquement `reports/com/AAAA-MM-JJ.md` et les visuels finaux
   `reports/com/AAAA-MM-JJ/`.
4. Transmettre à chaque agent : sa fiche, `editorial/communication.md`,
   `editorial/charte.md`, `editorial/identite.md`, et `editorial/voix.md` s'il existe.

## Ordre des agents

| # | Agent | Lit | Écrit |
|---|-------|-----|-------|
| 1 | Stratège (`01-stratege.md`) | Brief, rapport, `reports/com/` des 4 dernières semaines | `work/com/…/01-plan.md` |
| 2 | Plume sociale (`02-plume.md`) | plan, Brief, fiches | `work/com/…/02-textes.md` |
| 3 | Studio visuel (`03-studio.md`) | plan, textes, Brief | `work/com/…/visuels/` |
| 4 | Vigie et engagement (`05-vigie.md`) | `data/sources.json`, projets | `work/com/…/05-engagement.md` |
| 5 | Référenceur (`06-referenceur.md`) | le site construit (`dist/`) | `work/com/…/06-seo.md` |
| 6 | Diffuseur (`04-diffuseur.md`) | textes, visuels | brouillons Typefully, `work/com/…/04-diffusion.md` |
| 7 | Analyste (`08-analyste.md`) | rapport d'audience, statistiques Typefully | `work/com/…/08-analyse.md` |

Le premier lundi de chaque mois, lancer aussi **Relais et partenariats**
(`07-relais.md`) après la Vigie, et l'Analyste fait le bilan mensuel.

Un agent ne démarre que si le fichier du précédent existe et n'est pas vide. La Vigie et
le Référenceur sont indépendants : leur échec n'arrête pas le cycle, il est signalé.

## Fin du cycle

1. Assembler `reports/com/AAAA-MM-JJ.md` : à valider (les brouillons, par jour), à
   commenter (la Vigie), à corriger sur le site (le Référenceur), les chiffres (l'Analyste).
2. Commettre sur `com/AAAA-MM-JJ` et ouvrir une pull request vers `main` titrée
   « Communication de la semaine du AAAA-MM-JJ ».
3. Envoyer au rédacteur en chef un message court : nombre de brouillons prêts dans
   Typefully, jour par jour ; les 3 commentaires les plus utiles à poster ; une ligne de
   chiffres (abonnés gagnés, visites venues des réseaux).

## Arrêts

- Typefully indisponible : les textes restent dans le rapport, prêts à copier ; le dire
  en tête.
- Crédit Apify épuisé : la Vigie s'arrête, le reste continue.
- Un chiffre d'un brouillon ne correspond pas à la fiche du site : le brouillon est
  retiré et signalé. Jamais publié « à corriger plus tard ».
