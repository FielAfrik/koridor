"""Bilan d'audience hebdomadaire de Koridor (Umami Cloud).

Récupère les chiffres de la semaine écoulée (lundi 00:00 → dimanche 24:00, heure de Paris),
les compare à la semaine précédente et écrit :
  audience/AAAA-MM-JJ.json   données brutes et agrégées (AAAA-MM-JJ = lundi du rapport)
  audience/AAAA-MM-JJ.md     synthèse lisible, reprise par le Rapporteur
  audience/dernier.json      copie du plus récent, pour un accès simple

Usage :
  UMAMI_API_KEY=… python3 scripts/audience.py [--date AAAA-MM-JJ] [--out audience]
  UMAMI_SHARE_URL=https://cloud.umami.is/share/… python3 scripts/audience.py   # plan gratuit
  python3 scripts/audience.py --demo   # données fictives, pour tester la mise en forme

L'identifiant du site est lu dans site/config.json (analytics.website_id) ou dans
UMAMI_WEBSITE_ID. Sans clé ni identifiant, le script s'arrête proprement (code 0) en le
signalant, pour que le cycle de la semaine continue.
Aucune dépendance hors bibliothèque standard.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
TZ = ZoneInfo("Europe/Paris")
CONFIG = json.loads((ROOT / "site" / "config.json").read_text(encoding="utf-8"))
COUNTRIES = json.loads((ROOT / "site" / "countries.json").read_text(encoding="utf-8"))
COUNTRIES.update({k: v for k, v in {"FR": ["France"], "BE": ["Belgique"], "CH": ["Suisse"], "CA": ["Canada"],
                  "US": ["États-Unis"], "GB": ["Royaume-Uni"], "DE": ["Allemagne"], "NL": ["Pays-Bas"],
                  "ES": ["Espagne"], "IT": ["Italie"], "CN": ["Chine"], "AE": ["Émirats arabes unis"]}.items()
                  if k not in COUNTRIES})
PROJECTS = {p["id"]: p for p in json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))}
SECTORS = {"energie": "Énergie", "transport": "Transport", "eau": "Eau", "numerique": "Villes & numérique"}
API = os.environ.get("UMAMI_API_URL", "https://api.umami.is/v1").rstrip("/")
KEY = os.environ.get("UMAMI_API_KEY", "").strip()
SITE_ID = os.environ.get("UMAMI_WEBSITE_ID", "").strip() or (CONFIG.get("analytics") or {}).get("website_id", "")
# Plan gratuit sans clé d'API : lien de partage du tableau de bord (Website > Edit > Share URL).
SHARE_URL = os.environ.get("UMAMI_SHARE_URL", "").strip()
SHARE_TOKEN = ""


def use_share_link():
    """Échange le lien de partage contre un jeton de lecture, comme le fait la page publique.

    Sur Umami Cloud, l'API du tableau de bord vit sous /analytics/<région>/api (eu ou us).
    Le lien court cloud.umami.is/share/<id> ne dit pas la région : on essaie les deux.
    """
    global API, SHARE_TOKEN, SITE_ID
    u = urllib.parse.urlparse(SHARE_URL)
    parts = [x for x in u.path.split("/") if x]
    share_id = parts[parts.index("share") + 1]
    prefix = "/".join(parts[:parts.index("share")])
    bases = [f"{u.scheme}://{u.netloc}/{prefix}/api" if prefix else None] if prefix else []
    if "umami.is" in u.netloc and not prefix:
        bases = [f"{u.scheme}://{u.netloc}/analytics/{r}/api" for r in ("eu", "us")]
    bases.append(f"{u.scheme}://{u.netloc}/api")
    last = None
    for base in [b for b in bases if b]:
        req = urllib.request.Request(f"{base}/share/{share_id}", headers={"Accept": "application/json",
                                                                          "User-Agent": "koridor-audience/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                info = json.loads(r.read().decode("utf-8"))
        except (urllib.error.HTTPError, json.JSONDecodeError) as ex:
            last = ex
            continue
        if info.get("token"):
            API, SHARE_TOKEN = base, info["token"]
            SITE_ID = info.get("websiteId") or SITE_ID
            return
    raise RuntimeError(f"aucune adresse d'API n'a répondu ({last})")


# ---------- API ----------

def get(path, **params):
    q = urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    headers = {"Accept": "application/json", "User-Agent": "koridor-audience/1.0"}
    if SHARE_TOKEN:
        headers["x-umami-share-token"] = SHARE_TOKEN
        headers["x-umami-share-context"] = "1"   # exigé par Umami pour un jeton de partage
    else:
        headers["x-umami-api-key"] = KEY            # Umami Cloud
        headers["Authorization"] = f"Bearer {KEY}"  # forme indiquée dans la documentation récente
    req = urllib.request.Request(f"{API}{path}?{q}", headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8"))


def ms(dt):
    return int(dt.timestamp() * 1000)


def window(monday):
    start = datetime.combine(monday, time.min, TZ)
    return ms(start), ms(start + timedelta(days=7)) - 1


def num(v):
    """Umami renvoie selon les versions 12 ou {"value": 12, "prev": 9}."""
    if isinstance(v, dict):
        v = v.get("value")
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def stats(monday):
    a, b = window(monday)
    raw = get(f"/websites/{SITE_ID}/stats", startAt=a, endAt=b)
    out = {k: num(raw.get(k)) for k in ("pageviews", "visitors", "visits", "bounces", "totaltime")}
    return out


def metrics(monday, kind, limit=50):
    a, b = window(monday)
    kinds = [kind] if kind != "path" else ["path", "url"]   # « url » dans les anciennes versions
    for k in kinds:
        try:
            rows = get(f"/websites/{SITE_ID}/metrics", startAt=a, endAt=b, type=k, limit=limit)
            return [{"x": r.get("x") or "", "y": int(num(r.get("y")))} for r in rows]
        except urllib.error.HTTPError as ex:
            if ex.code != 400 or k == kinds[-1]:
                raise
    return []


# ---------- Agrégation ----------

def derived(s):
    visits = s["visits"] or 0
    return {
        "visiteurs": int(s["visitors"]),
        "visites": int(visits),
        "pages_vues": int(s["pageviews"]),
        "pages_par_visite": round(s["pageviews"] / visits, 1) if visits else 0,
        "duree_moyenne_s": round(s["totaltime"] / visits) if visits else 0,
        "taux_rebond": round(100 * s["bounces"] / visits) if visits else 0,
    }


def project_of(path):
    parts = [x for x in path.split("/") if x]
    for i, x in enumerate(parts):
        if x in ("projets", "projects") and i + 1 < len(parts):
            return parts[i + 1]
    return None


def group_events(rows):
    groups = {}
    for r in rows:
        cat, _, detail = r["x"].partition(" · ")
        groups.setdefault(cat.strip(), []).append({"detail": detail.strip(), "n": r["y"]})
    for v in groups.values():
        v.sort(key=lambda d: -d["n"])
    return groups


def build(monday_report, fetch):
    """monday_report : lundi du rapport ; la semaine mesurée est celle qui le précède."""
    week = monday_report - timedelta(days=7)
    prev = week - timedelta(days=7)
    cur, before = fetch["stats"](week), fetch["stats"](prev)
    trend = []
    for i in range(7, -1, -1):
        m = week - timedelta(days=7 * i)
        s = cur if i == 0 else before if i == 1 else fetch["stats"](m)
        trend.append({"semaine_du": m.isoformat(), "visiteurs": int(s["visitors"]), "pages_vues": int(s["pageviews"])})

    paths = fetch["metrics"](week, "path", 200)
    proj, langs, brief = {}, {"fr": 0, "en": 0}, 0
    for r in paths:
        pid = project_of(r["x"])
        if pid:
            proj[pid] = proj.get(pid, 0) + r["y"]
        seg = [x for x in r["x"].split("/") if x]
        for lg in ("fr", "en"):
            if lg in seg[:2]:
                langs[lg] += r["y"]
        if "brief" in seg:
            brief += r["y"]
    top_projects = [{"id": k, "nom": PROJECTS.get(k, {}).get("name", {}).get("fr", k), "vues": v}
                    for k, v in sorted(proj.items(), key=lambda kv: -kv[1])]
    never = [p["name"]["fr"] for k, p in PROJECTS.items() if k not in proj and p.get("status") != "brouillon"]

    events = group_events(fetch["metrics"](week, "event", 200))
    countries = [{"pays": (COUNTRIES.get(r["x"]) or [r["x"]])[0], "code": r["x"], "visiteurs": r["y"]}
                 for r in fetch["metrics"](week, "country", 15)]
    refs = [{"site": r["x"] or "(accès direct)", "visites": r["y"]} for r in fetch["metrics"](week, "referrer", 15)]
    devices = [{"type": r["x"], "visiteurs": r["y"]} for r in fetch["metrics"](week, "device", 10)]

    return {
        "rapport_du": monday_report.isoformat(),
        "periode": {"debut": week.isoformat(), "fin": (week + timedelta(days=6)).isoformat()},
        "semaine": derived(cur),
        "semaine_precedente": derived(before),
        "tendance_8_semaines": trend,
        "fiches_les_plus_lues": top_projects[:10],
        "fiches_sans_visite": never,
        "pages_brief": brief,
        "langue_pages_vues": langs,
        "provenance": refs,
        "pays": countries,
        "appareils": devices,
        "clics": events,
    }


# ---------- Mise en forme ----------

def evol(a, b):
    if not b:
        return "nouveau" if a else "="
    d = round(100 * (a - b) / b)
    return f"{'+' if d >= 0 else ''}{d} %"


def dur(s):
    return f"{s // 60} min {s % 60:02d} s" if s >= 60 else f"{s} s"


def top(events, cat, n=5, label=lambda d: d):
    rows = events.get(cat) or []
    return ", ".join(f"{label(r['detail'])} ({r['n']})" for r in rows[:n]) or "aucun"


def markdown(d):
    w, p = d["semaine"], d["semaine_precedente"]
    ev = d["clics"]
    fr = lambda x: f"{x:,}".replace(",", " ")
    L = [f"### Audience du site — semaine du {d['periode']['debut']} au {d['periode']['fin']}", "",
         "| Indicateur | Semaine | Semaine précédente | Évolution |", "|---|---:|---:|---:|"]
    for lab, k, f in (("Visiteurs uniques", "visiteurs", fr), ("Visites", "visites", fr), ("Pages vues", "pages_vues", fr),
                      ("Pages par visite", "pages_par_visite", lambda x: str(x).replace(".", ",")), ("Durée moyenne d'une visite", "duree_moyenne_s", dur),
                      ("Taux de rebond", "taux_rebond", lambda x: f"{x} %")):
        ch = f"{'+' if w[k] >= p[k] else ''}{w[k] - p[k]} pts" if k == "taux_rebond" else evol(w[k], p[k])
        L.append(f"| {lab} | {f(w[k])} | {f(p[k])} | {ch} |")
    L += ["", "**Tendance (visiteurs par semaine, 8 semaines)** : "
          + " → ".join(str(t["visiteurs"]) for t in d["tendance_8_semaines"]), ""]
    if d["fiches_les_plus_lues"]:
        L.append("**Fiches les plus lues** : " + ", ".join(f"{x['nom']} ({x['vues']})" for x in d["fiches_les_plus_lues"][:5]))
    if d["fiches_sans_visite"]:
        L.append(f"**Fiches sans aucune visite** ({len(d['fiches_sans_visite'])}) : " + ", ".join(d["fiches_sans_visite"][:8]))
    lg = d["langue_pages_vues"]
    tot = (lg["fr"] + lg["en"]) or 1
    L += [f"**Langue** : {round(100 * lg['fr'] / tot)} % des pages vues en français, {round(100 * lg['en'] / tot)} % en anglais. "
          f"Pages du Brief : {d['pages_brief']} vues.",
          "**Provenance** : " + (", ".join(f"{r['site']} ({r['visites']})" for r in d["provenance"][:5]) or "aucune"),
          "**Pays** : " + (", ".join(f"{r['pays']} ({r['visiteurs']})" for r in d["pays"][:6]) or "aucun"),
          "**Appareils** : " + (", ".join(f"{r['type']} ({r['visiteurs']})" for r in d["appareils"]) or "aucun"), "",
          "**Clics**", "",
          f"- Sources officielles consultées depuis les fiches : {top(ev, 'Source')}",
          f"- Modules qui envoient vers les fiches : {top(ev, 'Clic fiche')}",
          f"- Fiches lues jusqu'à la chronologie : {top(ev, 'Lecture complète', label=lambda x: PROJECTS.get(x, {}).get('name', {}).get('fr', x))}",
          f"- Filtres par secteur : {top(ev, 'Filtre secteur', label=lambda x: SECTORS.get(x, x or 'tous'))} ; par pays : "
          f"{top(ev, 'Filtre pays', label=lambda x: (COUNTRIES.get(x) or [x])[0])} ; carte : {top(ev, 'Carte', label=lambda x: (COUNTRIES.get(x) or [x])[0])}",
          f"- Recherches : {top(ev, 'Recherche', 8)}",
          f"- **Recherches sans résultat** (projets que les lecteurs cherchent et que Koridor ne suit pas) : {top(ev, 'Recherche sans résultat', 8)}",
          f"- Brief : {top(ev, 'Brief')} ; changement de langue : {top(ev, 'Langue')}"]
    return "\n".join(L) + "\n"


# ---------- Données fictives (--demo) ----------

def demo_fetch():
    import random
    rnd = random.Random(7)
    ids = list(PROJECTS)
    def st(m):
        v = rnd.randint(40, 160)
        return {"visitors": v, "visits": v * 1.3, "pageviews": v * 3.1, "bounces": v * 0.55, "totaltime": v * 1.3 * 140}
    def mt(m, kind, limit):
        if kind == "path":
            return [{"x": f"/koridor/fr/projets/{i}/", "y": rnd.randint(0, 40)} for i in ids[:-2]] + \
                   [{"x": "/koridor/en/projects/" + ids[0] + "/", "y": 12}, {"x": "/koridor/fr/brief/", "y": 18}]
        if kind == "event":
            return [{"x": "Source · afdb.org", "y": 14}, {"x": "Source · worldbank.org", "y": 9},
                    {"x": "Clic fiche · Liste des projets", "y": 31}, {"x": "Clic fiche · À la une", "y": 17},
                    {"x": "Lecture complète · " + ids[0], "y": 11}, {"x": "Filtre secteur · energie", "y": 8},
                    {"x": "Filtre pays · TG", "y": 6}, {"x": "Carte · CI", "y": 5}, {"x": "Recherche · lomé", "y": 4},
                    {"x": "Recherche sans résultat · inga", "y": 3}, {"x": "Brief · clic abonnement", "y": 7},
                    {"x": "Langue · en", "y": 5}]
        if kind == "country":
            return [{"x": "FR", "y": 40}, {"x": "TG", "y": 22}, {"x": "CI", "y": 15}, {"x": "MA", "y": 9}]
        if kind == "referrer":
            return [{"x": "linkedin.com", "y": 33}, {"x": "", "y": 25}, {"x": "google.com", "y": 12}]
        return [{"x": "mobile", "y": 52}, {"x": "laptop", "y": 30}, {"x": "desktop", "y": 18}]
    return {"stats": st, "metrics": mt}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="lundi du rapport (par défaut : lundi de cette semaine)")
    ap.add_argument("--out", default=str(ROOT / "audience"))
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()
    today = datetime.now(TZ).date()
    monday = date.fromisoformat(a.date) if a.date else today - timedelta(days=today.weekday())
    if a.demo:
        fetch = demo_fetch()
    else:
        if SHARE_URL and not KEY:
            try:
                use_share_link()
            except Exception as ex:  # noqa: BLE001
                print(f"Lien de partage Umami inutilisable ({ex}). Vérifier UMAMI_SHARE_URL.", file=sys.stderr)
                return 1
        elif not KEY or not SITE_ID:
            print("Mesure d'audience non configurée (ni UMAMI_API_KEY ni UMAMI_SHARE_URL) : rien à collecter.")
            return 0
        fetch = {"stats": stats, "metrics": metrics}
    try:
        data = build(monday, fetch)
    except urllib.error.HTTPError as ex:
        print(f"Échec de l'API Umami : HTTP {ex.code} {ex.reason}. Vérifier la clé et l'identifiant du site.", file=sys.stderr)
        return 1
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    js = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    (out / f"{monday.isoformat()}.json").write_text(js, encoding="utf-8")
    (out / "dernier.json").write_text(js, encoding="utf-8")
    (out / f"{monday.isoformat()}.md").write_text(markdown(data), encoding="utf-8")
    print(f"Audience écrite : {out}/{monday.isoformat()}.json et .md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
