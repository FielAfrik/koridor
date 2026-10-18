"""Prépare le plan de collecte de la semaine à partir du registre des sources.

Usage : python3 scripts/plan_collecte.py AAAA-MM-JJ
Écrit work/AAAA-MM-JJ/00-plan-collecte.json, que le Veilleur exécute avec les outils Apify.

Règles :
- priorité 1 : site, X et LinkedIn chaque semaine ;
- priorité 2 : site et X chaque semaine (pas de LinkedIn, pour tenir le budget) ;
- priorité 3 : site et X le premier lundi du mois seulement.
Seules les sources dont le statut est « actif » sont collectées.
"""
import json
import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Coûts unitaires Apify relevés en octobre 2026 (offre gratuite), en dollars.
X_ACTOR = "kaitoeasyapi/twitter-x-data-tweet-scraper-pay-per-result-cheapest"
COST_TWEET = 0.00025      # par tweet facturé
X_DUPLICATE_FACTOR = 2    # cet acteur renvoie souvent chaque tweet deux fois (dédoublonné à la fusion)
COST_LINKEDIN_POST = 0.002  # harvestapi/linkedin-company-posts, par post
COST_WEB_PAGE = 0.003     # apify/web-fetch, estimation par page rendue

MAX_QUERY_CHARS = 480     # longueur maximale d'une requête de recherche X
MAX_HANDLES_PER_QUERY = 10  # petits groupes : un compte bavard n'éteint pas les autres
TWEETS_PER_ACCOUNT = 20   # plafond moyen par compte et par semaine
LINKEDIN_POSTS_PER_PAGE = 6


def x_queries(handles, since, until):
    """Regroupe les comptes en requêtes « (from:a OR from:b …) since:… until:… »."""
    suffix = f" since:{since} until:{until}"
    queries, current = [], []
    for h in handles:
        trial = current + [h]
        text = "(" + " OR ".join(f"from:{x}" for x in trial) + ")" + suffix
        if (len(text) > MAX_QUERY_CHARS or len(trial) > MAX_HANDLES_PER_QUERY) and current:
            queries.append(current)
            current = [h]
        else:
            current = trial
    if current:
        queries.append(current)
    plans = []
    for group in queries:
        max_items = TWEETS_PER_ACCOUNT * len(group)
        plans.append({
            "handles": group,
            "searchTerm": "(" + " OR ".join(f"from:{x}" for x in group) + ")" + suffix,
            "maxItems": max_items,
            # L'acteur dépasse parfois maxItems : le plafond de dépense est la vraie limite.
            "maxTotalChargeUsd": round(max_items * X_DUPLICATE_FACTOR * COST_TWEET + 0.005, 3),
        })
    return plans


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage : python3 scripts/plan_collecte.py AAAA-MM-JJ")
    cycle = date.fromisoformat(sys.argv[1])
    since = (cycle - timedelta(days=7)).isoformat()
    until = cycle.isoformat()
    monthly = cycle.day <= 7  # premier lundi du mois

    sources = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    actives = [s for s in sources if s.get("status") == "actif"]
    selected = [s for s in actives if s["priority"] <= 2 or monthly]

    web = [{"id": s["id"], "url": s["web"]} for s in selected if s.get("web")]
    handles = [s["x"] for s in selected if s.get("x")]
    linkedin = [{"id": s["id"], "url": s["linkedin"]} for s in selected
                if s.get("linkedin") and s["priority"] == 1]
    data = [{"id": s["id"], "url": s["data"]["url"], "how": s["data"]["how"]}
            for s in selected if s.get("data")]

    queries = x_queries(handles, since, until)
    budget = {
        "x_max": round(sum(q["maxTotalChargeUsd"] for q in queries), 2),
        "linkedin_max": round(len(linkedin) * LINKEDIN_POSTS_PER_PAGE * COST_LINKEDIN_POST, 2),
        "web_estimate": round((len(web) + len(data)) * COST_WEB_PAGE, 2),
    }
    budget["total_max_usd"] = round(sum(budget.values()), 2)

    plan = {
        "cycle": until,
        "period": {"since": since, "until": until},
        "monthly_sources_included": monthly,
        "web": {
            "actor": "apify/web-fetch",
            "input": "url = chaque page ci-dessous, formats = [\"links\"]",
            "pages": web,
        },
        "data": {
            "actor": "apify/web-fetch",
            "input": "url = chaque adresse ci-dessous, formats = [\"raw\"] pour une API, [\"markdown\"] sinon",
            "endpoints": data,
        },
        "x": {
            "actor": X_ACTOR,
            "input": "un appel par requête : searchTerms = [searchTerm], queryType = \"Latest\", "
                     "maxItems = maxItems ; callOptions.maxTotalChargeUsd = maxTotalChargeUsd",
            "queries": queries,
        },
        "linkedin": {
            "actor": "harvestapi/linkedin-company-posts",
            "input": {"targetUrls": [p["url"] for p in linkedin], "postedLimit": "week",
                      "maxPosts": LINKEDIN_POSTS_PER_PAGE, "includeReposts": False},
            "pages": linkedin,
        },
        "budget_usd": budget,
    }
    out = ROOT / "work" / until / "00-plan-collecte.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{out.relative_to(ROOT)} : {len(web)} pages web, {len(data)} bases de données, "
          f"{len(handles)} comptes X en {len(queries)} requêtes, {len(linkedin)} pages LinkedIn. "
          f"Budget maximal : {budget['total_max_usd']} $")


if __name__ == "__main__":
    main()
