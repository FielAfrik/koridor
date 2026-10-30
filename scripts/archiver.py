"""Archivage des sources citées par Koridor (Wayback Machine) et contrôle des liens.

Pour chaque URL de source des jalons de data/projects.json :
  1. vérifie que la page répond encore (code HTTP) ;
  2. cherche une copie existante dans la Wayback Machine, sinon en demande une ;
  3. écrit l'état dans DOSSIER/archives.json (une entrée par URL) et un résumé lisible
     dans DOSSIER/etat.md, repris par le Rapporteur.

Usage :
  python3 scripts/archiver.py --out archives [--state archives/archives.json]
  python3 scripts/archiver.py --demo --out /tmp/archives   # sans réseau, pour tester

Options utiles : --limit (demandes d'archivage par exécution, 60 par défaut),
--delay (secondes entre deux demandes à la Wayback Machine, 5 par défaut),
--check-only (contrôle des liens sans demande d'archivage).

Règles : Wayback Machine seulement (pas d'Archive.today, voir
.claude/skills/archivage-sources/SKILL.md). Trois échecs d'archivage au plus par URL.
Le script ne sort jamais en erreur pour un site injoignable : il le note.
Aucune dépendance hors bibliothèque standard.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (compatible; KoridorArchiver/1.0; +https://github.com/FielAfrik/koridor)"
WAYBACK_RE = re.compile(r"/web/(\d{14})/")
MAX_ATTEMPTS = 3
BLOCKED = {401, 403, 429}


def cited_urls(projects):
    """URL de source -> projets qui la citent (ordre d'apparition conservé)."""
    out = {}
    for p in projects:
        for m in p.get("milestones") or []:
            for s in m.get("sources") or []:
                url = str(s.get("url") or "").strip()
                if url.startswith(("https://", "http://")):
                    ids = out.setdefault(url, [])
                    if p["id"] not in ids:
                        ids.append(p["id"])
    return out


class Net:
    """Accès réseau réel."""

    def status(self, url):
        for method in ("HEAD", "GET"):
            req = urllib.request.Request(url, method=method, headers={"User-Agent": UA})
            try:
                with urllib.request.urlopen(req, timeout=25) as r:
                    return r.status, None
            except urllib.error.HTTPError as ex:
                if method == "HEAD" and ex.code in (403, 404, 405, 501):
                    continue  # certains serveurs refusent HEAD : on retente en GET
                return ex.code, None
            except Exception as ex:  # DNS, délai, TLS
                if method == "HEAD":
                    continue
                return None, type(ex).__name__
        return None, "pas de réponse"

    def existing_copy(self, url):
        q = urllib.parse.urlencode({"url": url})
        req = urllib.request.Request(f"https://archive.org/wayback/available?{q}", headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read().decode("utf-8"))
        except Exception:
            return None
        snap = (data.get("archived_snapshots") or {}).get("closest") or {}
        if snap.get("available") and snap.get("url"):
            return snap["url"].replace("http://", "https://", 1)
        return None

    def save(self, url):
        target = "https://web.archive.org/save/" + urllib.parse.quote(urllib.parse.unquote(url), safe=":/?=&%")
        req = urllib.request.Request(target, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                final = r.geturl()
                link = r.headers.get("Content-Location") or ""
        except urllib.error.HTTPError as ex:
            return None, f"Wayback HTTP {ex.code}"
        except Exception as ex:
            return None, f"Wayback {type(ex).__name__}"
        for cand in (final, "https://web.archive.org" + link if link.startswith("/web/") else link):
            if cand and WAYBACK_RE.search(cand):
                return cand, None
        return None, "Wayback : pas d'adresse de copie renvoyée"


class DemoNet:
    """Réponses fictives et stables, pour tester sans réseau."""

    def status(self, url):
        n = sum(map(ord, url)) % 10
        if n == 0:
            return 404, None
        if n == 1:
            return 403, None
        if n == 2:
            return None, "URLError"
        return 200, None

    def existing_copy(self, url):
        if sum(map(ord, url)) % 3 == 0:
            return f"https://web.archive.org/web/20261020093000/{url}"
        return None

    def save(self, url):
        if sum(map(ord, url)) % 7 == 0:
            return None, "Wayback HTTP 523"
        return f"https://web.archive.org/web/20261102034500/{url}", None


def wayback_date(link):
    m = WAYBACK_RE.search(link or "")
    if not m:
        return None
    return f"{m.group(1)[:4]}-{m.group(1)[4:6]}-{m.group(1)[6:8]}"


def state_of(http, error):
    if http is not None and 200 <= http < 400:
        return "en ligne"
    if http in BLOCKED:
        return "lecture automatique refusée"
    return "injoignable"


def run(projects, previous, net, today, limit, delay, check_only, log):
    cited = cited_urls(projects)
    entries = {}
    for url, e in previous.items():
        entries[url] = dict(e)
        entries[url]["projects"] = []
    for url, ids in cited.items():
        e = entries.setdefault(url, {"first_seen": today, "http": None, "state": "non contrôlée",
                                     "wayback": None, "wayback_date": None, "attempts": 0, "error": None})
        e["projects"] = ids

    saved_now, requests_made = [], 0
    for url in cited:
        e = entries[url]
        http, err = net.status(url)
        e["http"], e["last_check"] = http, today
        e["state"] = state_of(http, err)
        e["error"] = err if e["state"] == "injoignable" and err else None
        if e.get("wayback") or check_only:
            continue
        if e.get("attempts", 0) >= MAX_ATTEMPTS:
            continue
        if requests_made >= limit:
            continue
        copy = net.existing_copy(url)
        if not copy and e["state"] != "injoignable":
            requests_made += 1
            copy, save_err = net.save(url)
            if delay:
                time.sleep(delay)
            if not copy:
                e["attempts"] = e.get("attempts", 0) + 1
                e["error"] = save_err
                log(f"échec d'archivage ({save_err}) : {url}")
        if copy:
            e["wayback"], e["wayback_date"], e["error"] = copy, wayback_date(copy), None
            saved_now.append(url)
    return entries, saved_now, requests_made


def summary(entries, saved_now, today, check_only):
    cited = {u: e for u, e in entries.items() if e.get("projects")}
    down = [(u, e) for u, e in cited.items() if e["state"] == "injoignable"]
    blocked = [(u, e) for u, e in cited.items() if e["state"] == "lecture automatique refusée"]
    no_copy = [(u, e) for u, e in cited.items() if not e.get("wayback")]
    given_up = [(u, e) for u, e in no_copy if e.get("attempts", 0) >= MAX_ATTEMPTS]
    lines = [f"# Archivage des sources, {today}", ""]
    lines += [
        "| Indicateur | Nombre |", "|---|---|",
        f"| Sources citées | {len(cited)} |",
        f"| Avec une copie Wayback | {len(cited) - len(no_copy)} |",
        f"| Copies obtenues à cette exécution | {len(saved_now)} |",
        f"| Pages injoignables | {len(down)} |",
        f"| Pages qui refusent la lecture automatique | {len(blocked)} |",
        "",
    ]
    if check_only:
        lines += ["Exécution en contrôle seul : aucune copie demandée.", ""]

    def block(title, items, with_copy=True):
        if not items:
            return []
        out = [f"## {title}", ""]
        for u, e in items:
            what = ", ".join(e["projects"])
            code = f"code {e['http']}" if e.get("http") else (e.get("error") or "pas de réponse")
            copy = f" ; copie du {e['wayback_date']} : {e['wayback']}" if with_copy and e.get("wayback") else (
                " ; aucune copie" if with_copy else "")
            out.append(f"- {what} : {u} ({code}){copy}")
        return out + [""]

    lines += block("Pages injoignables (à traiter avec le skill archivage-sources)", down)
    lines += block("Pages qui refusent la lecture automatique (à ouvrir à la main)", blocked)
    lines += block("Sans copie après trois essais (à signaler dans « À décider »)", given_up)
    if not (down or blocked or given_up):
        lines += ["Toutes les sources citées répondent et ont une copie, ou sont en cours d'archivage.", ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", default="archives")
    ap.add_argument("--state", help="archives.json de l'exécution précédente")
    ap.add_argument("--limit", type=int, default=60)
    ap.add_argument("--delay", type=float, default=5.0)
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--date", default=None, help="date du jour (AAAA-MM-JJ), pour les tests")
    args = ap.parse_args()

    today = args.date or datetime.now(timezone.utc).date().isoformat()
    date.fromisoformat(today)
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    previous = {}
    if args.state and Path(args.state).exists():
        previous = json.loads(Path(args.state).read_text(encoding="utf-8"))
    net = DemoNet() if args.demo else Net()
    delay = 0 if args.demo else args.delay
    entries, saved_now, n = run(projects, previous, net, today, args.limit, delay, args.check_only,
                                log=lambda msg: print(msg, file=sys.stderr))
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    (out / "archives.json").write_text(json.dumps(dict(sorted(entries.items())), ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8")
    (out / "etat.md").write_text(summary(entries, saved_now, today, args.check_only), encoding="utf-8")
    print(f"{len(entries)} URL suivies, {len(saved_now)} copies obtenues, {n} demandes d'archivage. "
          f"État écrit dans {out}/.")


if __name__ == "__main__":
    main()
