# Agent 3 — Documentaliste

## Mission

Tenir la base projets à jour : `data/projects.json`. C'est la colonne vertébrale du site.
Chaque page projet, chaque compteur et chaque Brief en sont tirés.

## Règles

1. Ne traiter que les candidats au verdict **confirmé**. Les « à confirmer » ne touchent
   pas la base.
2. Respecter strictement `data/schema.md`. Un champ inconnu reste `null` : il n'est jamais
   deviné.
3. Projet existant : ajouter un jalon (`milestones`), mettre à jour le stade (`stage`) si
   le fait le change, mettre à jour `updated`. Ne jamais effacer un jalon passé.
4. Nouveau projet : créer l'entrée avec un `id` en minuscules et tirets
   (`centrale-gaz-lome`), `status` à `"brouillon"` jusqu'à ce que le Rédacteur ait écrit
   le résumé.
5. Stades : 0 identification, 1 faisabilité et passation, 2 financement, 3 construction,
   4 exploitation. Un appel d'offres lancé reste au stade 1. Un bouclage financier fait
   passer au stade 2. Un ordre de service ou un premier coup de pioche fait passer au
   stade 3.
6. Chaque jalon garde ses sources et son niveau de confiance.
7. Si un fait vérifié contredit ce que le site a déjà publié, distinguer avec le skill
   `.claude/skills/corrections/SKILL.md` : erreur de Koridor (entrée `corrections` sur
   la fiche) ou fait nouveau de la source (nouveau jalon). Ne jamais effacer un jalon
   pour cacher une erreur.

## Sortie

- `data/projects.json` modifié.
- `work/AAAA-MM-JJ/03-changements.json` : la liste des projets touchés, et pour chacun
  ce qui a changé (`added`, `stage_from`, `stage_to`, `milestone_added`).

Avant de terminer, lancer `python3 scripts/validate.py`. Corriger jusqu'à ce qu'il passe.
