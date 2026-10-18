# Format des données

Tout le site est généré à partir de deux types de fichiers. `scripts/validate.py` vérifie
ce format à chaque pull request.

## `data/projects.json` — la base projets

Une liste d'objets :

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | texte | oui | Minuscules et tirets, unique, ne change jamais |
| `name` | `{fr, en}` | oui | Nom de l'ouvrage |
| `country` | texte | oui | Code ISO à 2 lettres (`CD`, `SN`, `TG`) ; plusieurs pays : `"ZM,ZW"` |
| `sector` | texte | oui | `energie`, `transport`, `eau` ou `numerique` |
| `stage` | entier 0–4 | oui | Voir la charte éditoriale |
| `status` | texte | oui | `brouillon`, `à vérifier` ou `publié` |
| `summary` | `{fr, en}` | si publié | 2 à 4 phrases |
| `capacity` | texte ou null | non | Telle qu'annoncée : `"500 MW"`, `"650 km"` |
| `cost` | objet ou null | non | `{amount, currency, unit, note: {fr, en}}` |
| `owner` | liste de textes | non | Maître d'ouvrage, sponsors |
| `lenders` | liste de textes | non | Bailleurs |
| `contractors` | liste de textes | non | EPC, entreprises |
| `target_date` | texte ou null | non | Mise en service visée, telle qu'annoncée |
| `milestones` | liste | oui (au moins 1) | Voir ci-dessous, du plus récent au plus ancien |
| `updated` | date | oui | `AAAA-MM-JJ` |

Un jalon :

```json
{
  "date": "2026-10-14",
  "type": "financement",
  "text": {"fr": "…", "en": "…"},
  "confidence": "confirmé",
  "sources": [{"url": "https://…", "publisher": "…", "title": "…", "published": "2026-10-14", "tier": "A"}]
}
```

`type` : `annonce`, `etude`, `appel-d-offres`, `attribution`, `signature`, `financement`,
`travaux`, `mise-en-service`, `retard`, `reglementation`.
`confidence` : `confirmé` ou `à confirmer`.

## `data/briefs/AAAA-MM-JJ.json` — le Brief du lundi

```json
{
  "date": "2026-10-19",
  "number": 1,
  "moved": [{"project_id": "metro-kinshasa", "line": {"fr": "…", "en": "…"}}],
  "deal": {"project_id": "metro-kinshasa", "title": {"fr": "…", "en": "…"}, "body": {"fr": "…", "en": "…"}},
  "analysis": {"title": {"fr": "…", "en": "…"}, "body": {"fr": "…", "en": "…"}}
}
```

Les paragraphes de `body` sont séparés par une ligne vide.
