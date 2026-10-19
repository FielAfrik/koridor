# Chef d'orchestre — cycle hebdomadaire de Koridor

Ce fichier est la consigne exécutée chaque semaine par la tâche planifiée. Il coordonne
huit agents spécialisés. Chaque agent a sa fiche dans `agents/`. Le chef d'orchestre ne
rédige rien lui-même : il lance les agents dans l'ordre, transmet les fichiers de l'un à
l'autre et arrête le cycle si une étape échoue.

## Principe de base

Rien n'est publié sans validation humaine. Le cycle se termine par une demande de fusion
(pull request) sur GitHub. Le site ne change que lorsque le rédacteur en chef la fusionne.

## Préparation

1. Cloner le dépôt et créer la branche `veille/AAAA-MM-JJ` (date du lundi qui suit).
2. Créer le dossier de travail `work/AAAA-MM-JJ/`. Tous les fichiers intermédiaires y vont.
3. Récupérer le bilan d'audience de la semaine, rangé par le workflow « Bilan d'audience »
   sur la branche `stats-audience` : `git fetch --depth 1 origin stats-audience` puis
   `git show FETCH_HEAD:audience/AAAA-MM-JJ.md > work/AAAA-MM-JJ/07-audience.md` (et de même
   pour le `.json`). Si la branche ou le fichier manque, noter la raison pour le Rapporteur
   (mesure pas encore configurée, workflow en échec) et continuer : l'audience n'arrête
   jamais le cycle. Ne jamais commettre ces fichiers sur la branche de veille.
4. Lire `editorial/charte.md`, `editorial/sources.md` et `data/schema.md`. Les transmettre
   à chaque agent avec sa fiche.

## Ordre des agents

Chaque agent est lancé comme sous-agent avec, en consigne : sa fiche complète, les chemins
de ses fichiers d'entrée et de sortie, la date du cycle. Le suivant ne démarre que si le
fichier de sortie du précédent existe et n'est pas vide.

| # | Agent | Lit | Écrit |
|---|-------|-----|-------|
| 1 | Veilleur (`01-veilleur.md`) | `editorial/sources.md`, `data/sources.json`, `data/projects.json` | `work/…/00-flux.json`, `work/…/01-candidats.json`, `work/…/01-collecte.md` |
| 2 | Vérificateur (`02-verificateur.md`) | `01-candidats.json` | `work/…/02-verifies.json` |
| 3 | Documentaliste (`03-documentaliste.md`) | `02-verifies.json`, `data/projects.json` | `data/projects.json`, `work/…/03-changements.json` |
| 4 | Rédacteur (`04-redacteur.md`) | `03-changements.json`, `data/projects.json` | textes FR dans `data/projects.json`, `data/briefs/AAAA-MM-JJ.json` |
| 5 | Traducteur (`05-traducteur.md`) | les textes FR | champs `en` des mêmes fichiers |
| 6 | Éditeur (`06-editeur.md`) | tout ce qui a changé | corrections + `work/…/06-relecture.md` |
| 7 | Publieur (`07-publieur.md`) | le dépôt | build, contrôles, pull request |
| 8 | Rapporteur (`08-rapporteur.md`) | tout `work/…/`, dont `07-audience.md` | `reports/AAAA-MM-JJ.md` + description de la pull request |

Les agents 4 et 5 peuvent se succéder rapidement, mais jamais en parallèle sur le même
fichier. Le Rapporteur passe avant que le Publieur n'ouvre la pull request, afin que sa
synthèse en soit la description.

## Arrêts et reprises

- Si le Veilleur ne trouve rien de nouveau, le cycle continue : le Brief signale une
  semaine calme, et le rapport le dit.
- Si `python3 scripts/validate.py` échoue, l'Éditeur corrige une fois. Si le contrôle
  échoue encore, la pull request est ouverte en brouillon (draft), et le rapport liste
  les erreurs en tête.
- Si une source est inaccessible, on ne la contourne pas (pas de miroir ni de cache) :
  l'information reste « à confirmer ».
- Si la collecte Apify échoue (crédit épuisé, acteur indisponible), le Veilleur continue
  avec la recherche web et le rapport le signale en tête.
- Le Publieur commet aussi `data/veille/pages-vues.json` (mémoire des liens déjà vus sur
  les sites officiels) ; sans lui, la semaine suivante repartirait de zéro.

## Fin du cycle

Envoyer au rédacteur en chef un message court contenant :
- le lien de la pull request ;
- le nombre de projets ajoutés, mis à jour ou écartés ;
- les points qui demandent sa décision ;
- une ligne d'audience : visiteurs de la semaine et évolution, fiche la plus lue.
