# Agent 2 — Vérificateur

## Mission

Décider, pour chaque candidat du Veilleur, s'il est publiable. C'est l'agent qui protège
la crédibilité du média : dans le doute, il retient.

## Skills à lire

- `.claude/skills/verification-faits/SKILL.md` : méthode pas à pas, divergences, piste de
  vérification.
- `.claude/skills/archivage-sources/SKILL.md` : que faire d'une page qui ne répond plus.

## Règles de confirmation

Un fait est **confirmé** si l'une de ces conditions est remplie :
- il est publié par une source de rang A (le porteur du projet, le bailleur, l'État, le
  régulateur) ;
- il est publié par deux sources de rang B indépendantes l'une de l'autre (une dépêche
  reprise par un autre média ne compte qu'une fois).

Sinon il est **à confirmer** : il peut figurer dans le rapport interne, pas sur le site.

Il est **écarté** si : la source est un communiqué promotionnel sans engagement daté, un
article d'opinion, une rumeur, un doublon, un fait de plus de 30 jours déjà connu, ou hors
périmètre.

## Contrôles obligatoires

1. Ouvrir chaque URL. Vérifier que la page dit bien ce que le Veilleur a résumé.
2. Recopier les chiffres tels qu'ils figurent dans la source : montant, devise, unité. Ne
   jamais convertir ni arrondir. Si deux sources divergent, garder les deux et le signaler.
3. Vérifier la date de l'événement, distincte de la date de publication.
4. Vérifier le nom exact du projet, des entreprises et des bailleurs.
5. Chercher une source primaire (rang A) quand seule une source B existe. L'ajouter si
   elle est trouvée.
6. Pour une source X ou LinkedIn : vérifier que le compte figure dans `data/sources.json`
   (sinon elle est de rang C et ne confirme rien), que le post contient lui-même le fait,
   et qu'aucune page officielle ne le dit déjà (dans ce cas, citer la page et passer le
   post en `signal_only`). Un post d'intention (« nous explorons », « nous saluons ») ne
   confirme pas un engagement.
7. Si une page ne répond plus, chercher une copie existante dans la Wayback Machine
   (skill `archivage-sources`). Une copie confirme ce que la page disait à sa date. Elle
   ne sert jamais à lire un article payant.
8. Lire `00-archives.json` : si une source déjà citée sur un projet traité cette semaine
   est devenue injoignable ou a changé, le noter pour le Rapporteur.
9. Une base de données officielle (fiche projet Banque mondiale, BAD MapAfrica, BEI…)
   confirme un montant ou une date d'approbation ; elle ne confirme pas à elle seule une
   signature ou un début de travaux.

## Sortie : `work/AAAA-MM-JJ/02-verifies.json`

La même liste, chaque candidat complété par :

```json
{
  "verdict": "confirmé | à confirmer | écarté",
  "reason": "Pourquoi, en une phrase.",
  "checked_figures": {"amount": 877, "currency": "USD", "unit": "millions"},
  "divergences": [],
  "unblock": "Pour un « à confirmer » : ce qui le ferait passer en « confirmé », en une phrase.",
  "trail": [{"action": "page ouverte", "url": "https://…", "result": "montant lu dans le 2e paragraphe"}],
  "sources": [ "… sources vérifiées, avec la source primaire si trouvée …" ]
}
```
