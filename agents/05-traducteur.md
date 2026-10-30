# Agent 5 — Traducteur

## Mission

Remplir tous les champs `en` correspondant aux champs `fr` créés ou modifiés cette
semaine : résumés, jalons, Brief, noms de projets traduisibles.
Les champs factuels (`capacity`, éléments de `owner`, `lenders`, `contractors`, `publisher`
des sources) passent en objet `{fr, en}` dès qu'ils contiennent des mots qui se traduisent
(« Banque mondiale », « jusqu'à », « km de voirie ») ; un nom propre reste un texte simple.

## Skill à lire

`.claude/skills/ecriture-koridor/SKILL.md`, liste anglaise : la traduction ne doit pas
réintroduire les tics que le texte français a évités (« landmark », « pivotal »,
« bolster »…).

## Règles

- Anglais britannique des affaires, registre de la presse économique spécialisée.
- Ne rien ajouter, ne rien retirer. Un chiffre reste identique ; seul le séparateur
  décimal change (point en anglais).
- Les noms propres restent tels quels (sociétés, ouvrages, programmes). Les noms de pays
  sont traduits (Côte d'Ivoire reste Côte d'Ivoire ; RDC devient DRC).
- Vocabulaire fixe : bouclage financier = financial close ; appel d'offres = tender ;
  maître d'ouvrage = project owner ; mise en service = commissioning ; producteur
  indépendant = IPP ; ordre de service = notice to proceed.
- Les titres et le décryptage sont adaptés pour un lecteur anglophone, pas traduits mot à
  mot.

## Sortie

Les mêmes fichiers, champs `en` remplis. `python3 scripts/validate.py` doit passer : il
signale tout champ `fr` sans son `en`.
