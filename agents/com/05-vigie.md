# C5 — Vigie et engagement

## Mission

Trouver les conversations du secteur où Koridor a quelque chose d'utile à dire, et
préparer les réponses aux commentaires reçus.

## Étapes

1. **Posts à commenter** : relever, avec Apify, les publications des 7 derniers jours
   des comptes LinkedIn et X officiels de `data/sources.json` (banques de développement,
   ministères, agences) qui parlent d'un projet suivi par Koridor. Retenir les 5 où un
   commentaire peut apporter un fait ou un repère (le stade du projet, une échéance, un
   projet comparable), jamais une simple félicitation.
2. **Mentions de Koridor** : chercher « Koridor » et l'adresse du site sur LinkedIn et X.
3. **Commentaires reçus** sur les posts de la semaine précédente : préparer une réponse
   pour chacun de ceux qui posent une question ou apportent une information.

## Sortie : `work/com/AAAA-MM-JJ/05-engagement.md`

Pour chaque post : le lien, l'auteur, en une ligne de quoi il parle, et un brouillon de
commentaire de 300 caractères au plus, au nom du rédacteur en chef.

## Règles

- **L'agent ne commente, ne réagit, ne s'abonne et n'écrit à personne.** Il prépare ;
  le rédacteur en chef poste.
- Un commentaire n'inclut pas de lien vers Koridor, sauf si on lui pose la question.
- Pas de collecte de données personnelles : on garde le lien du post et le nom du compte
  institutionnel, rien sur les personnes qui commentent.
- Budget Apify : la veille sociale passe après la collecte éditoriale. Si le crédit du
  mois descend sous 1 dollar, la Vigie s'arrête et le signale.
