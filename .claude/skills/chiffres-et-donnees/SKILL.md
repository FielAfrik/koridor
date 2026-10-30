---
name: chiffres-et-donnees
description: Manipuler les chiffres et les jeux de données de Koridor (montants, capacités, totaux, comparaisons, graphiques, chiffres d'audience) sans erreur d'unité ni conclusion abusive. À utiliser par le Rédacteur pour le décryptage, l'Éditeur, le Studio visuel et l'Analyste.
---

# Chiffres et données

Adapté de `data-journalism` (collection claude-skills-journalism de Joe Amditis,
licence MIT, voir `../README.md`), ramené aux usages de Koridor : une base de projets,
des montants annoncés dans plusieurs devises, des cartes et des visuels, des chiffres
d'audience faibles au démarrage.

## Règles de base (rappel de la charte)

- Montant, devise et unité tels que la source les écrit. Pas de conversion, pas
  d'arrondi.
- Chaque chiffre publié existe dans `data/projects.json` ou dans un Brief, et renvoie à
  une source vérifiée.
- Une estimation est signalée comme telle et attribuée.

## Totaux et comparaisons

- On n'additionne pas des montants de devises différentes. « 877 millions de dollars et
  120 millions d'euros », pas « environ 1 milliard ».
- On n'additionne pas des périmètres différents : le coût total d'un projet et la part
  d'un bailleur ne s'ajoutent pas. Le champ `cost.note` dit de quel périmètre il s'agit.
- Un total sur la base (« 14 projets solaires suivis ») dit sur quoi il porte : les
  projets suivis par Koridor, pas tous les projets du pays.
- Une comparaison se fait entre choses comparables : MW avec MW, MWc avec MWc, même
  année. Une capacité installée n'est pas une production (MW contre GWh).
- Un ratio (dollars par MW, coût au kilomètre) n'est publié que si les deux chiffres
  viennent de la même source ou de sources A concordantes, et il est présenté comme un
  calcul de Koridor dans un texte étiqueté « Analyse ».
- Une hausse ou une baisse se donne avec ses deux valeurs et ses deux dates.

## Contrôles avant d'utiliser un chiffre

1. Unité : millions ou milliards ? kW, MW ou GW ? kV ? m³ par jour ou par an ?
2. Devise : dollar américain, euro, franc CFA (XOF ou XAF), rand, naira, dirham ?
3. Date : à quelle date le chiffre est-il valable (approbation, signature, mise à jour
   d'un coût) ?
4. Périmètre : projet entier, une phase, une tranche, la part d'un bailleur ?
5. Ordre de grandeur : le chiffre est-il cohérent avec les projets comparables de la
   base ? Un écart d'un facteur 10 ou 1 000 signale presque toujours une erreur d'unité :
   on revérifie la source avant toute chose.

## Graphiques et visuels (Studio visuel, carte)

- Chaque visuel porte sa source, son unité et sa date.
- Axe des barres à zéro. Pas de troisième dimension, pas de camembert au-delà de quatre
  parts.
- Pas de graphique qui mélange des devises ou des unités sur un même axe.
- Un visuel qui montre un chiffre le montre à l'identique de la fiche du site (même
  séparateur, même unité). Le Studio relit chaque chiffre contre `data/projects.json`
  avant d'exporter.
- Texte alternatif pour chaque visuel publié sur le site : ce que montre le graphique,
  en une phrase avec les chiffres principaux.

## Données ouvertes des bailleurs

Les bases de la Banque mondiale, de la BAD (MapAfrica), de la BEI ou d'IATI peuvent
servir au décryptage. Avant usage :
- noter l'URL exacte, la date de consultation et la période couverte ;
- vérifier la date de dernière mise à jour (l'API projets de la Banque mondiale s'arrête
  à décembre 2024, voir `editorial/sources.md`) ;
- garder la donnée brute dans `work/AAAA-MM-JJ/donnees/` sans la modifier, et faire les
  calculs sur une copie ;
- écrire dans le décryptage d'où vient la donnée et ce qu'elle ne couvre pas.

## Chiffres d'audience (Analyste, Rapporteur)

- Les chiffres d'Umami et de Typefully sont repris tels quels.
- Sous 50 visiteurs par semaine ou 500 impressions par post, on ne tire aucune
  conclusion d'une variation (règle déjà fixée dans les fiches de l'Analyste et du
  Rapporteur).
- Une part se donne avec son effectif : « 12 % (18 visites sur 150) ».
- Une corrélation entre un post et un pic de visites n'est pas une preuve : on vérifie
  la provenance (`utm_source`, référent) avant d'attribuer les visites à un canal.

## Registre des chiffres du décryptage

Pour le décryptage (300 à 500 mots), le Rédacteur tient dans
`work/AAAA-MM-JJ/04-chiffres.md` une ligne par chiffre utilisé : le chiffre tel
qu'écrit, le projet et le champ de la base d'où il vient (ou l'URL de la donnée
ouverte), et le calcul s'il y en a un. L'Éditeur contrôle le décryptage contre ce
registre.
