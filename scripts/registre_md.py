"""Génère editorial/registre.md, la version lisible du registre data/sources.json.

Usage : python3 scripts/registre_md.py
À relancer après chaque modification du registre (le Veilleur le fait s'il ajoute une source).
"""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GROUPS = [
    ("Banques multilatérales et institutions de financement", {"mdb"}),
    ("Bailleurs bilatéraux", {"dfi"}),
    ("Institutions continentales et régionales", {"regional", "pool"}),
    ("Agences internationales", {"agency"}),
    ("États : gouvernements et ministères", {"gov", "ministry"}),
    ("Régulateurs", {"regulator"}),
    ("Sociétés publiques et agences nationales", {"utility", "agency_nat"}),
    ("PPP, investissement, marchés publics et transport", {"ppp", "invest", "procurement", "transport"}),
    ("Bases de données ouvertes", {"data"}),
]
STATUS = {"actif": "✅ actif", "à vérifier": "⚠️ à vérifier", "référence": "📚 référence"}


def cell(text):
    return str(text or "").replace("|", "/").replace("\n", " ")


def main():
    sources = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    by_type = defaultdict(list)
    for s in sources:
        by_type[s["type"]].append(s)

    actives = [s for s in sources if s["status"] == "actif"]
    lines = [
        "# Registre des sources officielles",
        "",
        "Fichier généré par `scripts/registre_md.py` à partir de `data/sources.json`. "
        "Ne pas le modifier à la main : modifier le registre, puis relancer le script.",
        "",
        f"**{len(sources)} sources**, dont {len(actives)} actives : "
        f"{sum(1 for s in actives if s.get('web'))} sites, "
        f"{sum(1 for s in actives if s.get('x'))} comptes X, "
        f"{sum(1 for s in actives if s.get('linkedin'))} pages LinkedIn. "
        "Priorité 1 : collecte hebdomadaire sur tous les canaux ; 2 : site et X chaque semaine ; "
        "3 : une fois par mois. Les règles sont dans `editorial/sources.md`.",
        "",
    ]
    for title, types in GROUPS:
        rows = sorted((s for t in types for s in by_type.get(t, [])),
                      key=lambda s: (s["priority"], s["country"], s["name"]))
        if not rows:
            continue
        lines += [f"## {title} ({len(rows)})", "",
                  "| Source | Pays | Prio. | Site | X | LinkedIn | Statut | Remarque |",
                  "|---|---|---|---|---|---|---|---|"]
        for s in rows:
            web = f"[site]({s['web']})" if s.get("web") else ("injoignable" if s.get("web_check") == "injoignable" else "—")
            if s.get("web") and s.get("web_check") == "à confirmer":
                web += " (à confirmer)"
            x = f"[@{s['x']}](https://x.com/{s['x']})" if s.get("x") else "—"
            li = f"[page]({s['linkedin']})" if s.get("linkedin") else "—"
            lines.append(f"| {cell(s['name'])} | {s['country']} | {s['priority']} | {web} | {x} | {li} | "
                         f"{STATUS.get(s['status'], s['status'])} | {cell(s.get('notes'))} |")
        lines.append("")
    out = ROOT / "editorial" / "registre.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"{out.relative_to(ROOT)} : {len(sources)} sources.")


if __name__ == "__main__":
    main()
