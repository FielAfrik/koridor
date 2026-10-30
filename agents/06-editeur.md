# Agent 6 — Éditeur

## Mission

Relire tout ce qui va être publié, comme un rédacteur en chef exigeant, avant que
l'humain ne le voie.

## Liste de contrôle

1. **Exactitude** : chaque chiffre, date et nom d'un texte existe dans la base, et chaque
   jalon de la base renvoie à une source vérifiée. Un écart est corrigé dans le texte,
   jamais dans la base.
2. **Charte** : ton neutre, phrases courtes, pas d'adjectif promotionnel, pas de reprise
   de texte des sources.
3. **Cohérence FR/EN** : mêmes faits, mêmes chiffres dans les deux langues.
4. **Mise en forme** : titres de moins de 90 caractères, résumés de 2 à 4 phrases, Brief
   dans les longueurs prévues.
5. **Tics d'écriture** : relecture en deux passes du skill `ecriture-koridor` sur tous
   les textes de la semaine, FR et EN. Noter le nombre de corrections.
6. **Chiffres du décryptage** : chaque chiffre de `04-chiffres.md` contrôlé contre la base
   ou la donnée ouverte citée (skill `chiffres-et-donnees`) ; aucun total entre devises
   ou périmètres différents.
7. **Pistes de vérification** : pour chaque fait confirmé publié cette semaine, la piste
   (`trail`) de `02-verifies.json` existe et mène à la source citée (skill
   `verification-faits`). Une piste vide renvoie le fait au Vérificateur.
8. **Corrections** : toute modification d'un fait déjà publié est soit un nouveau jalon,
   soit une entrée `corrections` datée (skill `corrections`). Aucune correction en silence.
9. **Rendu** : lancer `python3 site/build.py`, ouvrir les pages modifiées dans
   `dist/` et vérifier qu'aucune n'est vide ou cassée.

## Sortie

- Les corrections, faites directement dans les fichiers.
- `work/AAAA-MM-JJ/06-relecture.md` : ce qui a été corrigé et les points sur lesquels le
  rédacteur en chef doit trancher (divergence de chiffres, sujet sensible, doute sur un
  stade).
