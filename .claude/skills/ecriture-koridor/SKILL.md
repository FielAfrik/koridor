---
name: ecriture-koridor
description: Écrire et relire les textes de Koridor (fiches, jalons, Brief, posts) sans les tics d'écriture des modèles de langue, en français et en anglais. À utiliser par le Rédacteur, le Traducteur, l'Éditeur et la Plume sociale, avant de rendre tout texte.
---

# Écriture Koridor

Adapté de `ai-writing-detox` (collection claude-skills-journalism de Joe Amditis,
licence MIT, voir `../README.md`), réécrit pour le français et pour la charte de Koridor.
La règle de base de l'original vaut ici : un lecteur qui remarque le style ne lit plus
le fait. Les tournures typiques des modèles de langue se repèrent vite et coûtent la
confiance d'un lecteur professionnel.

Ce skill complète `editorial/charte.md`. En cas de doute, la charte l'emporte.

## Fond

1. Des faits : qui, quoi, quand, combien, où. Aucune phrase sur l'importance, le
   « tournant » ou le « contexte plus large » d'un projet sans un fait qui la porte.
2. Pas de fin de phrase accrochée par un participe qui commente : « …, soulignant son
   rôle », « …, illustrant l'importance de… », « …, témoignant de… ». On coupe.
3. Relations exactes : « finance », « construit », « exploite », « a signé ». Jamais
   « associé à », « lié à », « impliqué dans » quand le rôle est connu.
4. Attribution précise : on nomme l'institution. Jamais « selon les experts » ou « de
   nombreux observateurs » pour une seule source.
5. Pas de schéma « Défis / Perspectives », pas de « Malgré ses atouts, X fait face à des
   défis », pas de paragraphe final qui résume. Le texte s'arrête quand l'information est
   donnée. Le décryptage finit sur un fait à suivre ou une date.
6. Pas de précautions oratoires : « il est important de noter », « il convient de
   souligner », « à considérer comme indicatif ».

## Vocabulaire à remplacer (français)

| À éviter | À la place |
|---|---|
| crucial, essentiel, primordial, incontournable, clé (adjectif) | le fait qui le montre, ou rien |
| véritable, réel (en intensif) | supprimer |
| robuste | solide, ou décrire (« dimensionné pour 1 000 MW ») |
| constituer, représenter, se positionner comme, servir de | être, avoir |
| offrir, proposer (quand « a » suffit) | avoir |
| témoigner de, souligner, mettre en lumière, mettre en exergue | montrer, ou supprimer |
| s'inscrire dans | faire partie de, ou supprimer |
| jouer un rôle clé ou central | dire le rôle : « finance 40 % » |
| favoriser, renforcer, tirer parti, levier | le verbe exact : « finance », « relie », « ajoute 300 MW » |
| paysage, écosystème (au figuré) | secteur, marché |
| naviguer, plonger dans (au figuré) | supprimer |
| en constante évolution, à l'ère de, dans un monde où | supprimer |
| de plus, en outre, par ailleurs (en début de phrase) | commencer par le fait |
| en somme, en définitive | supprimer la phrase de résumé |
| ambitieux, historique, révolutionnaire, majeur, emblématique, phare | supprimer (charte, règle 5) |
| recourir à, tenter de, procéder à | utiliser, essayer, faire |

## Vocabulaire à remplacer (anglais)

additionally, align with, boasts, bolster, crucial, delve, emphasize, enhance, foster,
garner, highlight, interplay, intricate, landscape, leverage, meticulous, multifaceted,
navigate, pivotal, realm, robust, seamless, showcase, tapestry, testament, underscore,
vibrant, game-changer, landmark, flagship. Remplacer par le verbe ou le chiffre exact.
« Over » pour une quantité devient « more than ».

## Syntaxe

- « est », « a », « il y a » plutôt que des verbes de substitution.
- Pas de contraste plaqué : « non seulement… mais aussi », « ce n'est pas X, c'est Y »,
  « plus qu'un X, un Y ».
- Pas de série de trois par réflexe. On énumère le nombre réel d'éléments.
- Longueur des phrases variée selon le propos ; pas de phrase choc isolée en fin de
  paragraphe. La charte fixe la limite haute : 25 mots.
- Verbe direct : « a signé » plutôt que « a procédé à la signature ».
- Un mot répété vaut mieux qu'un synonyme forcé (« le projet », « le projet », pas
  « l'infrastructure », « l'ouvrage », « l'initiative » pour la même chose).
- Affirmations nettes quand la source les porte (« la première centrale solaire
  flottante du pays » si la source le dit et qu'on l'a vérifié), nuances ordinaires
  sinon.

## Forme

- Aucun tiret cadratin (—) dans les textes publiés : virgule, deux-points, parenthèses
  ou point.
- Guillemets « » en français, " " en anglais.
- Pas d'emoji, pas de gras dans les posts.
- Titres : majuscule au premier mot seulement, sujet + verbe + fait (charte).

## Relecture en deux passes

1. Passe de recherche : chercher dans le texte chaque mot des deux listes, les
   tirets cadratins, les tournures « non seulement », « ce n'est pas », les participes
   en fin de phrase. Corriger chaque occurrence.
2. Passe de lecture : relire comme un ingénieur EPC pressé. Chaque phrase doit lui
   apprendre quelque chose. Une phrase qui ne contient ni nom, ni chiffre, ni date, ni
   verbe d'action précis est supprimée ou réécrite.

L'Éditeur note dans `06-relecture.md` le nombre de corrections faites à ce titre ; si un
même tic revient trois semaines de suite, il propose de l'ajouter à la consigne de
l'agent qui le produit.

## Exemples

Exemples fictifs, inventés pour montrer la réécriture : ne pas les reprendre comme des
faits.

Avant : « Ce financement historique témoigne de l'engagement renforcé de la BAD en
faveur de la transition énergétique, s'inscrivant dans une dynamique régionale plus
large. »
Après : « La BAD prête 120 millions de dollars à la Senelec pour 225 km de lignes 225 kV
entre Tambacounda et Kédougou. »

Avant : « Not only does the project bolster grid stability, it also showcases Kenya's
pivotal role in the region. »
After : « The 400 kV line adds 1,500 MW of transfer capacity between Kenya and
Tanzania. »
