"""Fusionne les collectes brutes de la semaine en un seul flux trié, relié au registre.

Usage : python3 scripts/fusion_flux.py AAAA-MM-JJ

Lit dans work/AAAA-MM-JJ/ (fichiers écrits par le Veilleur, absents = canal ignoré) :
- 00-brut-x.json         éléments renvoyés par l'acteur X du plan (champs plats ou imbriqués)
- 00-brut-linkedin.json  éléments renvoyés par harvestapi/linkedin-company-posts
- 00-brut-web.json       liste de {"id", "url", "links": [...]} (apify/web-fetch, format links)

Écrit work/AAAA-MM-JJ/00-flux.json : une entrée par publication, avec la source du
registre, le canal, la date, l'URL, le texte et un indicateur de pertinence.

Pour les sites, seuls les liens apparus depuis la semaine précédente sont gardés. La
mémoire des liens déjà vus est data/veille/pages-vues.json, mise à jour par ce script et
versionnée avec la pull request. À la première collecte d'un site, ses liens servent de
référence et rien n'est signalé comme nouveau.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "data" / "veille" / "pages-vues.json"

KEYWORDS = [
    # énergie
    "énergi", "energ", "électri", "electri", "power", "solaire", "solar", "éolien", "wind",
    "hydro", "barrage", "dam", "centrale", "plant", "mw", "gw", "kv", "réseau", "grid",
    "transmission", "interconnex", "mini-grid", "mini-réseau", "gaz", "gas", "hydrogène",
    "hydrogen", "batter", "stockage", "storage", "géotherm", "geotherm", "mission 300",
    # infrastructures
    "route", "road", "autoroute", "highway", "pont", "bridge", "port", "rail", "chemin de fer",
    "railway", "aéroport", "airport", "métro", "metro", "corridor", "logisti", "eau potable",
    "water", "assainissement", "sanitation", "dessalement", "desalination", "irrigation",
    "fibre", "fiber", "data center", "datacenter", "câble", "cable", "infrastruct",
    # étapes de projet
    "financement", "financing", "prêt", "loan", "don ", "grant", "garantie", "guarantee",
    "approuv", "approv", "signature", "sign", "accord", "agreement", "appel d'offres",
    "tender", "attribu", "award", "ppp", "concession", "epc", "bouclage", "financial close",
    "mise en service", "commission", "inaugur", "première pierre", "groundbreaking",
    "lancement", "launch", "travaux", "construction", "projet", "project",
]


def get(item, dotted, default=None):
    """Lit un champ, que l'élément soit plat (« author.userName ») ou imbriqué."""
    if dotted in item:
        return item[dotted]
    cur = item
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return default
        cur = cur[part]
    return cur


def relevant(text):
    low = (text or "").lower()
    return any(k in low for k in KEYWORDS)


def load(path):
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def norm_linkedin(url):
    m = re.search(r"linkedin\.com/(company|school|showcase|in)/([^/?#]+)", url or "", re.I)
    return f"{m.group(1).lower()}/{m.group(2).lower()}" if m else None


def article_like(link, base):
    """Garde les liens internes qui ressemblent à une page de contenu."""
    u = urlparse(link)
    b = urlparse(base)
    if u.scheme not in ("http", "https"):
        return False
    host = u.netloc.lower().removeprefix("www.")
    if host != b.netloc.lower().removeprefix("www."):
        return False
    path = u.path.rstrip("/")
    if path.count("/") < 2 or "#" in link:
        return False
    if re.search(r"(page=|/page/\d|/tag/|/category/|/categorie/|/search|/contact|/about|"
                 r"/a-propos|/careers|/emploi|/countries/|/pays/|\.(jpg|png|css|js)$)", link, re.I):
        return False
    return True


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage : python3 scripts/fusion_flux.py AAAA-MM-JJ")
    cycle = sys.argv[1]
    work = ROOT / "work" / cycle
    sources = json.loads((ROOT / "data" / "sources.json").read_text(encoding="utf-8"))
    by_id = {s["id"]: s for s in sources}
    by_x = {s["x"].lower(): s for s in sources if s.get("x")}
    by_li = {norm_linkedin(s["linkedin"]): s for s in sources if s.get("linkedin")}

    flux, unknown, seen_urls = [], [], set()

    def add(src, channel, published, url, text, links=None):
        key = (url or "").split("?")[0].lower()
        if key and key in seen_urls:  # les acteurs X renvoient parfois un tweet deux fois
            return
        seen_urls.add(key)
        flux.append({
            "source_id": src["id"] if src else None,
            "source": src["name"] if src else None,
            "country": src["country"] if src else None,
            "tier": "A" if src else "C",
            "channel": channel,
            "published": published,
            "url": url,
            "text": (text or "").strip()[:1500],
            "links": links or [],
            "pertinent": relevant(text),
        })

    # X
    for t in load(work / "00-brut-x.json") or []:
        handle = str(get(t, "author.userName") or "").lower()
        src = by_x.get(handle)
        if not src:
            unknown.append(f"x:{handle}")
        urls = get(t, "entities.urls") or []
        links = [u.get("expanded_url") for u in urls if isinstance(u, dict) and u.get("expanded_url")]
        if not links and get(t, "entities.urls.expanded_url"):
            links = [get(t, "entities.urls.expanded_url")]
        add(src, "x", get(t, "createdAt"), get(t, "url"), get(t, "fullText") or get(t, "text"), links)

    # LinkedIn
    for p in load(work / "00-brut-linkedin.json") or []:
        key = norm_linkedin(get(p, "query.targetUrl")) or norm_linkedin(get(p, "author.linkedinUrl"))
        src = by_li.get(key)
        if not src:
            unknown.append(f"linkedin:{key}")
        add(src, "linkedin", get(p, "postedAt.date"), get(p, "linkedinUrl"), get(p, "content"))

    # Sites officiels : nouveaux liens depuis la dernière collecte
    state = load(STATE) or {}
    baseline = []
    for page in load(work / "00-brut-web.json") or []:
        src = by_id.get(page.get("id"))
        base = page.get("url") or (src or {}).get("web") or ""
        links = sorted({l.split("#")[0] for l in page.get("links") or [] if article_like(l, base)})
        seen = set(state.get(page.get("id"), []))
        if not seen:
            baseline.append(page.get("id"))
        else:
            for link in links:
                if link not in seen:
                    slug = urlparse(link).path.rstrip("/").rsplit("/", 1)[-1].replace("-", " ")
                    add(src, "web", None, link, slug)
        state[page.get("id")] = sorted(seen | set(links))[-400:]

    if (work / "00-brut-web.json").exists():
        STATE.parent.mkdir(parents=True, exist_ok=True)
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                         encoding="utf-8")

    flux.sort(key=lambda e: (not e["pertinent"], e["channel"], e["source_id"] or ""))
    out = work / "00-flux.json"
    out.write_text(json.dumps(flux, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts = {}
    for e in flux:
        counts[e["channel"]] = counts.get(e["channel"], 0) + 1
    print(f"{out.relative_to(ROOT)} : {len(flux)} publications "
          f"({', '.join(f'{k} {v}' for k, v in sorted(counts.items())) or 'aucune'}), "
          f"dont {sum(e['pertinent'] for e in flux)} pertinentes.")
    if baseline:
        print(f"Première collecte (référence posée, rien de signalé) : {', '.join(baseline)}")
    if unknown:
        print(f"Comptes absents du registre, traités en rang C : {', '.join(sorted(set(unknown)))}")


if __name__ == "__main__":
    main()
