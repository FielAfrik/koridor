# Sources de Koridor

Koridor s'appuie d'abord sur les **émetteurs officiels** : banques multilatérales de
développement (MDB), bailleurs bilatéraux, institutions régionales, États, régulateurs,
sociétés publiques et agences reconnues. La presse spécialisée sert à repérer et à
recouper, jamais à remplacer une source officielle quand celle-ci existe.

Le registre complet, avec les adresses vérifiées, est `data/sources.json` (version lisible :
`editorial/registre.md`). Ce fichier-ci
fixe les règles. Toute source ajoutée ou retirée passe par une pull request.

## Principe : le rang dépend de l'émetteur, pas du canal

Une annonce de la BAD reste une source de rang A, qu'elle paraisse sur afdb.org, sur son
compte X ou sur sa page LinkedIn. Inversement, un article de presse reste de rang B même
s'il est relayé par un compte officiel.

| Canal | Rang A si… | Sinon |
|---|---|---|
| Site officiel (communiqué, avis, décision, base projets) | le domaine est celui de l'institution, inscrit au registre | — |
| Compte X officiel | le compte figure au registre **et** il est lié depuis le site officiel de l'institution | rang C |
| Page LinkedIn officielle | même condition que pour X | rang C |
| Base de données ouverte (Banque mondiale, BAD MapAfrica, BEI, AFD, IFC, IATI) | elle est publiée par l'institution elle-même | — |
| Journal officiel, bulletin des marchés publics | publié par l'État ou l'autorité compétente | — |
| Compte personnel d'un ministre, d'un DG ou d'un président de MDB | jamais seul : il signale, la source officielle confirme | rang C |

### Ce qui fait foi sur les réseaux sociaux

1. On cherche toujours la page officielle liée au post (communiqué, fiche projet). Si elle
   existe, c'est **elle** qu'on cite, et le post n'est qu'un signal.
2. Si le fait n'est publié que sur le compte officiel (cas fréquent pour les signatures
   et cérémonies annoncées par un ministère ou une société d'électricité), le post peut
   être cité comme source de rang A, à trois conditions : le compte est au registre, le
   post contient lui-même le fait (montant, partie, date), et son texte est conservé dans
   `work/…/00-flux.json` au cas où il serait supprimé.
3. Un post qui dit « nous avons discuté », « nous explorons », « nous saluons » n'est pas un
   engagement : il est écarté ou reste « à confirmer ».
4. Les comptes de service client (pannes, factures) sont exclus du registre.

### Comment un compte entre au registre

Un compte X ou LinkedIn n'est inscrit que s'il est **lié depuis le site officiel** de
l'institution (en-tête, pied de page ou page presse). C'est ainsi qu'ont été relevés les
comptes du registre le 18 octobre 2026. Un compte trouvé par une recherche, même certifié
par la plateforme, reste « à vérifier » tant que ce lien n'a pas été constaté.

## Rang A — émetteurs officiels (un fait confirmé à lui seul)

Familles de sources, détaillées dans `data/sources.json` :

- **Banques multilatérales et institutions de financement du développement** : BAD,
  Groupe Banque mondiale (BIRD/IDA, IFC, MIGA), BEI, BID, Afreximbank, AFC, Africa50,
  TDB, BOAD, BIDC, BDEAC, DBSA, BADEA, OPEC Fund, Fonds vert pour le climat…
- **Bailleurs bilatéraux** : AFD et Proparco, KfW et DEG, FMO, BII, DFC, JICA, Norfund,
  Commission européenne (Global Gateway), fonds arabes.
- **Institutions continentales et régionales** : Union africaine, AUDA-NEPAD et PIDA,
  CEDEAO, UEMOA, CEEAC, EAC, SADC, pools énergétiques (EEEOA/WAPP, EAPP, SAPP, PEAC),
  organismes de bassin (OMVS, OMVG), CEB.
- **États** : présidences, primatures et gouvernements, ministères de l'énergie, des
  infrastructures et des transports, unités PPP, agences de promotion des investissements.
- **Régulateurs et sociétés publiques** : régulateurs de l'électricité (ARSE, ANARE-CI,
  CRSE, ANRE, NERC, EPRA, NERSA…), sociétés d'électricité (CEET, CIE, CI-Énergies,
  Senelec, ONEE, MASEN, Eskom, KPLC…), agences d'électrification rurale, ports.
- **Agences internationales de référence** : IRENA, AIE, SEforALL — pour les données et
  les rapports, pas pour les annonces de projets.
- **Porteurs de projets** : communiqués officiels des développeurs, EPC et fonds.

## Rang B — presse spécialisée (deux sources indépendantes pour confirmer)

- Agence Ecofin et ses déclinaisons pays (Togo First, Investir au Cameroun…)
- African Energy (africa-energy.com) ; ESI Africa ; Energy Capital & Power
- The Africa Report ; Jeune Afrique ; African Business
- Construction Review Online ; IJGlobal / Green Street (partiellement payants)
- Reuters, Bloomberg, Financial Times (partiellement payants)

## Rang C — repérage seulement (jamais une source de publication)

- Comptes sociaux absents du registre, comptes personnels, forums, agrégateurs, sites
  sans auteur ni date.

## Fréquence de collecte

| Priorité | Site officiel | X | LinkedIn |
|---|---|---|---|
| 1 — acteurs clés et pays prioritaires | chaque semaine | chaque semaine | chaque semaine |
| 2 — acteurs importants | chaque semaine | chaque semaine | non |
| 3 — veille large | premier lundi du mois | premier lundi du mois | non |

Le plan de la semaine est calculé par `scripts/plan_collecte.py`, qui affiche aussi le
budget Apify maximal. La fusion des collectes est faite par `scripts/fusion_flux.py`.

## Points d'attention relevés lors de la vérification du 18 octobre 2026

- L'API publique des projets de la Banque mondiale répond, mais ses dernières
  approbations datent de décembre 2024 : elle ne suffit pas à suivre l'actualité. Les
  communiqués et le compte X Banque mondiale Afrique prennent le relais.
- Le domaine edc-cameroon.org redirige vers un site sans rapport : il est retiré du
  registre jusqu'à confirmation de la nouvelle adresse d'EDC.
- Le site de l'Autorité du bassin du Niger affiche des liens sociaux de démonstration :
  aucun compte n'est retenu.
- Plusieurs sites publics ne répondent pas à une lecture automatique (voir le statut
  « injoignable » dans le registre). Ils sont retentés chaque mois, et leurs comptes
  sociaux, s'ils sont connus, prennent le relais.

## Sources payantes

Le titre d'un article payant peut signaler un sujet. Le fait n'est publiable que s'il est
confirmé par des sources accessibles. On ne contourne jamais un accès payant.
