---
name: archivage-sources
description: Conserver une copie datée de chaque source citée par Koridor (Wayback Machine) et retrouver une page disparue ou modifiée. À utiliser par le Vérificateur, l'Éditeur et le Rapporteur, et dès qu'une source citée ne répond plus.
---

# Archivage des sources

Adapté de `web-archiving` (collection claude-skills-journalism de Joe Amditis, licence
MIT, voir `../README.md`), réduit à ce dont Koridor a besoin.

## Pourquoi

Un ministère retire un communiqué, une société d'électricité supprime un post, un
bailleur déplace sa page projet. La fiche Koridor renvoie alors vers une page vide, et le
chiffre publié n'a plus de preuve consultable. Une copie datée chez un tiers garde la
preuve de ce que la source disait le jour où on l'a citée.

## Ce qui est archivé, et par qui

Le workflow « Archivage des sources » (`.github/workflows/archives.yml`) lance
`scripts/archiver.py` :
- chaque lundi à 3 h 40 (heure d'hiver de Paris), avant le cycle de veille ;
- après chaque fusion qui modifie `data/projects.json`, pour archiver tout de suite les
  sources de la semaine ;
- à la demande, depuis l'onglet Actions.

Le script :
1. relève toutes les URL de sources des jalons de `data/projects.json` ;
2. vérifie que chaque page répond encore (code HTTP) ;
3. demande une copie à la Wayback Machine pour chaque URL qui n'en a pas encore ;
4. range l'état sur la branche `archives-sources` : `archives/archives.json` (une
   entrée par URL) et `archives/etat.md` (le résumé lisible).

Cette branche ne contient que l'état de l'archivage. Elle ne touche ni `main` ni le site.

Les agents n'archivent pas eux-mêmes pendant le cycle : leur environnement ne joint pas
toujours archive.org, et le workflow s'en charge après la fusion.

## Services retenus

| Service | Usage chez Koridor |
|---|---|
| Wayback Machine (web.archive.org) | Service unique d'archivage. Copie publique, datée, citable. |
| Archive.today | Non utilisé. Il sert souvent à contourner les accès payants, ce que la charte interdit, et son statut juridique est contesté depuis fin 2025. |
| Perma.cc | Non utilisé (compte payant, usage juridique). À reconsidérer si un litige l'exige. |
| Caches de Google ou Bing | Fermés depuis 2024. |

## Lire l'état de l'archivage

Le chef d'orchestre copie au début du cycle `archives/archives.json` dans
`work/AAAA-MM-JJ/00-archives.json` et `archives/etat.md` dans
`work/AAAA-MM-JJ/00-archives.md`. Chaque entrée :

```json
"https://www.afdb.org/fr/news-and-events/press-releases/…": {
  "projects": ["metro-kinshasa"],
  "first_seen": "2026-10-26",
  "last_check": "2026-11-02",
  "http": 200,
  "state": "en ligne",
  "wayback": "https://web.archive.org/web/20261027081500/https://www.afdb.org/…",
  "wayback_date": "2026-10-27",
  "error": null
}
```

`state` vaut `en ligne`, `injoignable` (la page ne répond pas ou renvoie une erreur) ou
`non contrôlée` (pas encore testée). `wayback` est vide tant que la copie n'existe pas.

## Quand une source citée ne répond plus

1. Ne pas retirer le jalon, ne pas changer son niveau de confiance : la source a existé
   et a été vérifiée.
2. Relire la copie Wayback (`wayback`) pour vérifier que le chiffre publié y figure.
3. Chercher si l'institution a déplacé la page (même titre sur son site). Si oui,
   proposer la nouvelle URL dans la pull request, avec l'ancienne en note.
4. Si la page a été retirée et qu'il n'existe aucune copie, le signaler dans « À
   décider » : le rédacteur en chef choisit entre garder le jalon avec la mention de la
   source retirée et le repasser « à confirmer ».
5. Si la page a changé et contredit désormais la fiche (montant revu, date décalée),
   c'est un fait nouveau ou une correction : voir le skill `corrections`.

## Quand le Vérificateur peut consulter une archive

- Pour lire une page officielle qui ne répond plus pendant la vérification : on cherche
  une copie existante avec `https://archive.org/wayback/available?url=URL` (via
  `apify/web-fetch`). La copie confirme ce que la page disait à sa date, pas ce qu'elle
  dit aujourd'hui.
- Jamais pour lire un article payant : une archive ne sert pas à contourner un accès
  payant ou bloqué (charte et `editorial/sources.md`).

## Limites connues

- La Wayback Machine refuse certaines pages (robots.txt du site, pages très lourdes en
  JavaScript, PDF de plus de quelques dizaines de mégaoctets). L'entrée garde alors
  `error` et le script réessaie la semaine suivante, trois fois au plus.
- Sans compte, la Wayback Machine accepte environ 15 demandes par minute. Le script
  attend entre deux demandes et s'arrête à 60 URL par exécution ; le reste passe à
  l'exécution suivante.
- Un post LinkedIn n'est souvent pas archivable sans connexion. Son texte est conservé
  dans `00-flux.json`, et c'est cette copie qui fait foi (`editorial/sources.md`).
