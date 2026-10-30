---
name: corrections
description: Corriger une erreur publiée sur Koridor de façon visible et datée (fiche projet, Brief, post). À utiliser par le Documentaliste, l'Éditeur, le Rapporteur et la Plume sociale dès qu'un fait publié se révèle faux, incomplet ou dépassé.
---

# Corrections

Adapté de la partie « Corrections » de `fact-check-workflow` (collection
claude-skills-journalism de Joe Amditis, licence MIT, voir `../README.md`). La charte
promet qu'une erreur publiée est corrigée et que la correction est datée sur la page :
ce skill dit comment.

## Correction, mise à jour ou fait nouveau

| Situation | Ce qu'on fait |
|---|---|
| Le site a publié un chiffre, une date ou un nom faux (erreur de Koridor ou de la source) | Correction : on rectifie et on ajoute une entrée `corrections` à la fiche |
| La source a elle-même changé un chiffre après publication (montant revu, calendrier décalé) | Fait nouveau : nouveau jalon daté, l'ancien jalon reste |
| Une information manquait sans rendre le texte faux | Mise à jour : on complète, `updated` change, pas d'entrée `corrections` |
| Un lien de source est mort | Ni l'un ni l'autre : voir le skill `archivage-sources` |

On ne corrige jamais en silence. On n'efface jamais un jalon passé pour faire
disparaître une erreur : on rectifie son texte et on le dit.

## Format dans `data/projects.json`

Champ optionnel `corrections`, du plus récent au plus ancien :

```json
"corrections": [
  {
    "date": "2026-11-02",
    "text": {
      "fr": "Une version précédente indiquait un financement de 877 millions d'euros. Le communiqué de la BAD indique 877 millions de dollars.",
      "en": "An earlier version gave the financing as EUR 877 million. The AfDB press release gives USD 877 million."
    }
  }
]
```

Règles du texte :
- ce qui était écrit, puis ce qui est exact, avec la source ;
- une ou deux phrases, ton neutre, sans formule d'excuse ;
- la date est celle de la correction, pas celle de l'erreur.

Le site affiche ces entrées dans un encadré « Corrections » en bas de la fiche.
`scripts/validate.py` contrôle le format.

## Brief déjà paru

Un Brief publié ne se réécrit pas en silence. On corrige le texte du fichier
`data/briefs/AAAA-MM-JJ.json` concerné et on ajoute la correction à la fiche du projet.
Le Brief suivant mentionne la correction en une ligne dans la rubrique Méthode des
réseaux (vendredi, voir `editorial/communication.md`).

## Posts déjà publiés

Les agents ne touchent pas aux posts publiés. Le Diffuseur prépare dans Typefully un
brouillon de commentaire de correction, à poster par le rédacteur en chef sous le post
d'origine : ce qui était écrit, ce qui est exact, le lien vers la fiche corrigée
(commentaire, donc hors corps du post).

## Journal des corrections

Le Rapporteur liste chaque semaine, dans une rubrique « Corrections » du rapport :
la fiche, l'erreur, la correction, comment l'erreur a été repérée (relecture, lecteur,
source qui a changé, archivage), et l'étape du cycle qui aurait dû l'arrêter. Au bout de
trois corrections venues de la même étape, il propose une règle de plus pour l'agent
concerné.
