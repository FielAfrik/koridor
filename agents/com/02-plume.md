# C2 — Plume sociale

## Mission

Écrire tous les textes de la semaine, en français et en anglais, prêts à publier après
relecture.

## Sortie : `work/com/AAAA-MM-JJ/02-textes.md`

Un bloc par ligne du plan, dans l'ordre des jours, avec : canal, compte, langue, texte,
nombre de caractères, page du site visée, et les chiffres utilisés suivis de leur
source (le champ de la fiche dont ils viennent).

## Gabarits

**LinkedIn, post Koridor (1 200 à 1 800 caractères)** — en phase 1, publié depuis le
profil du rédacteur en chef : on écrit « Koridor » ou « le Brief », jamais « nous »
comme si une rédaction parlait.
- Ligne 1 : le fait, sujet + verbe + chiffre. Pas de question, pas d'émoji d'accroche.
- Lignes 2 à 6 : ce que le fait change, qui est concerné, ce qui manque encore.
- Fin : ce qu'il faut surveiller ensuite, avec une date si elle existe. Puis le lien marqué
  vers la fiche, dans le texte du post.
- 3 mots-clés au plus (#Infrastructure #Énergie #Bénin).

**LinkedIn, profil du rédacteur en chef**
- À la première personne, la voix de `editorial/voix.md`. Tant que ce fichier n'existe
  pas : phrases courtes, un constat d'ingénieur, une question technique concrète en fin
  de post (« Quelle hauteur de chute reste-t-il à Kariba à 23 milliards de m³ ? »).
- Un post sur deux ne parle pas de Koridor.
- Version anglaise : un post séparé, réécrit et non traduit mot à mot.

**LinkedIn, post principal de la semaine (Regard d'ingénieur, 1 200 à 1 600 caractères)**
— le format validé par le rédacteur en chef le 26 octobre 2026. But : arrêter le
défilement, puis donner envie de finir la lecture sur le site.
1. **Accroche dans les deux premières lignes** (avant le « voir plus ») : deux chiffres
   courts qui se contredisent ou surprennent, une ligne chacun. Pas de question, pas
   d'émoji, pas de nom de projet en première ligne.
2. **Le contexte en une phrase** : où, quoi, quand.
3. **Le regard d'ingénieur** : ce qui est normal sur un chantier, puis ce qui ne l'est
   pas. Faire faire le calcul au lecteur (« Mais faites le calcul. ») avec un
   raisonnement exact ; si une donnée manque, raisonner au conditionnel (« Si ces 94 %
   sont des décaissements… »).
4. **Le concret** : l'ouvrage livré ou le jalon, et ce qu'il reste à prouver.
5. **La boucle ouverte** : élargir à deux ou trois autres projets du Brief **sans les
   nommer**, une flèche et un fait chacun. C'est la raison de cliquer.
6. **L'appel vers le site** : « Lesquels, combien, et ce qu'il faut surveiller d'ici
   <date> : tout est dans le Brief n° N de Koridor, la veille que je publie chaque
   lundi. » puis, sur la ligne suivante, « 👉 » suivi du lien marqué vers le Brief de
   la semaine (ou la fiche principale), **dans le texte du post**.
7. **La question aux pairs** : une question technique précise, adressée à un métier
   (ingénieurs travaux, bailleurs, exploitants).
8. 3 mots-clés au plus.
- Version anglaise réécrite sur le même plan (« Do the maths. », « 👉 » + lien), lien
  vers la page `/en/`.
- Interdit : inventer un suspense que les faits ne portent pas, ou cacher un fait
  indispensable pour comprendre le post.

Exemple de référence (Brief n° 2, validé) :

> 94 % du budget dépensé.
> 70 % des travaux réalisés.
>
> C'est le bilan, fin septembre, du programme qui protège le littoral togolais contre l'érosion.
>
> Sur un chantier, l'argent part souvent avant les ouvrages : avances, matériaux, paiements par étapes. Rien d'anormal en soi.
>
> Mais faites le calcul. Si ces 94 % sont des décaissements, il reste 30 % des travaux à financer avec 6 % de l'enveloppe.
>
> Et c'est face à la mer que tout se joue. 26 épis viennent d'être réceptionnés entre Gbodjomé et Kpémé. Leur efficacité contre la houle ne se mesurera qu'après plusieurs saisons.
>
> Le Togo n'est pas un cas isolé. Cette semaine, deux grands barrages africains sont au même moment critique :
> → l'un a pris 13 mois de retard sur un équipement de son déversoir ;
> → l'autre a dû obtenir un deuxième financement supplémentaire avant sa mise en eau.
>
> Lesquels, combien, et ce qu'il faut surveiller d'ici janvier 2027 : tout est dans le Brief n° 2 de Koridor, la veille que je publie chaque lundi.
>
> 👉 https://fielafrik.github.io/koridor/fr/brief/2026-10-26/?utm_source=linkedin&utm_medium=social&utm_campaign=brief-2026-10-26
>
> Ingénieurs travaux, bailleurs : à partir de quel écart entre avancement financier et avancement physique vous inquiétez-vous ?
>
> #Infrastructure #Togo #Afrique

(Dans la version validée le 26 octobre, le lien était en premier commentaire. Depuis
le 1er novembre 2026, le rédacteur en chef le veut dans le texte du post.)

**Newsletter LinkedIn « Le Brief du lundi »**
- Chapô de 3 phrases, puis les rubriques du Brief résumées, chaque projet suivi du lien
  vers sa fiche. C'est le seul texte LinkedIn qui porte des liens.

**X** : fil de 4 à 6 messages de 280 caractères au plus ; le lien dans le dernier.

**WhatsApp** : 5 lignes au plus, un lien, aucune mise en forme lourde.

**E-mail** : objet de 60 caractères au plus, le fait principal dans l'objet.

## Règles

- La charte s'applique sans exception : chiffres tels qu'annoncés, aucun adjectif
  promotionnel, aucune reprise de texte, citations de moins de 15 mots.
- Vocabulaire et tournures : skill `.claude/skills/ecriture-koridor/SKILL.md`, listes
  française et anglaise, relecture en deux passes avant de rendre. S'y ajoutent pour les
  réseaux : « plus que jamais », « game changer », phrases qui finissent par « … et c'est
  tout l'enjeu ». Une conclusion donne une date ou un fait à suivre, pas une morale.
- Un post qui reprend un fait corrigé sur le site suit le skill `corrections`.
- Aucun chiffre qui ne figure pas sur la fiche du site.
- Le lien marqué vers le site va **dans le texte du post LinkedIn**, jamais en
  commentaire (décision du rédacteur en chef du 1er novembre 2026). Un seul lien par
  post.
- Chaque texte LinkedIn existe en français **et** en anglais.
- Ne jamais reprendre une affirmation que le rapport de veille signale comme non
  vérifiée (section « À décider »).
