"""Contrôle du format des données avant publication.

Usage : python3 scripts/validate.py
Sort avec le code 1 et liste les erreurs si un fichier ne respecte pas data/schema.md.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECTORS = {"energie", "transport", "eau", "numerique"}
STATUSES = {"brouillon", "à vérifier", "publié"}
CONFIDENCE = {"confirmé", "à confirmer"}
TYPES = {"annonce", "etude", "appel-d-offres", "attribution", "signature", "financement",
         "travaux", "mise-en-service", "retard", "reglementation"}
TIERS = {"A", "B"}
DATE_RE = re.compile(r"^\d{4}-\d{2}(-\d{2})?$")
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

errors = []


def err(where, msg):
    errors.append(f"{where} : {msg}")


def bilingual(where, value, required=True):
    if value is None:
        if required:
            err(where, "texte manquant")
        return
    if not isinstance(value, dict):
        err(where, "doit être un objet {fr, en}")
        return
    for lang in ("fr", "en"):
        if not str(value.get(lang) or "").strip():
            err(where, f"version « {lang} » manquante")


def check_source(where, src):
    url = str(src.get("url") or "")
    if not url.startswith("https://") and not url.startswith("http://"):
        err(where, "URL de source invalide")
    if not src.get("publisher"):
        err(where, "éditeur de la source manquant")
    elif isinstance(src.get("publisher"), dict):
        bilingual(f"{where}, éditeur", src["publisher"])
    if src.get("tier") not in TIERS:
        err(where, "rang de source A ou B attendu")
    pub = src.get("published")
    if pub is not None and not DATE_RE.match(str(pub)):
        err(where, "date de publication invalide")


def check_projects(countries):
    path = ROOT / "data" / "projects.json"
    try:
        projects = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        err("data/projects.json", f"JSON invalide ({e})")
        return {}
    seen = {}
    for i, p in enumerate(projects):
        pid = p.get("id") or f"#{i}"
        w = f"projet {pid}"
        if not ID_RE.match(str(p.get("id") or "")):
            err(w, "identifiant invalide (minuscules et tirets)")
        if pid in seen:
            err(w, "identifiant en double")
        seen[pid] = p
        bilingual(f"{w}, nom", p.get("name"))
        for code in str(p.get("country") or "").split(","):
            if code.strip() not in countries:
                err(w, f"code pays inconnu « {code} »")
        if p.get("sector") not in SECTORS:
            err(w, f"secteur inconnu « {p.get('sector')} »")
        if p.get("stage") not in range(5):
            err(w, "stade entre 0 et 4 attendu")
        if p.get("status") not in STATUSES:
            err(w, f"statut inconnu « {p.get('status')} »")
        if p.get("status") in ("publié", "à vérifier"):
            bilingual(f"{w}, résumé", p.get("summary"))
        # Champs factuels : texte neutre (nom propre, chiffre) ou objet {fr, en}
        if isinstance(p.get("capacity"), dict):
            bilingual(f"{w}, capacité", p.get("capacity"))
        for field in ("owner", "lenders", "contractors"):
            for k, x in enumerate(p.get(field) or []):
                if isinstance(x, dict):
                    bilingual(f"{w}, {field} {k + 1}", x)
                elif not isinstance(x, str) or not x.strip():
                    err(w, f"{field} {k + 1} : texte ou objet {{fr, en}} attendu")
        if p.get("cost"):
            c = p["cost"]
            if not isinstance(c.get("amount"), (int, float)):
                err(w, "montant du coût non numérique")
            bilingual(f"{w}, note de coût", c.get("note"), required=False)
        if not DATE_RE.match(str(p.get("updated") or "")):
            err(w, "date de mise à jour invalide")
        ms = p.get("milestones") or []
        if not ms:
            err(w, "au moins un jalon est requis")
        for j, m in enumerate(ms):
            mw = f"{w}, jalon {j + 1}"
            if not DATE_RE.match(str(m.get("date") or "")):
                err(mw, "date invalide (AAAA-MM ou AAAA-MM-JJ)")
            if m.get("type") not in TYPES:
                err(mw, f"type inconnu « {m.get('type')} »")
            if m.get("confidence") not in CONFIDENCE:
                err(mw, "confiance « confirmé » ou « à confirmer » attendue")
            bilingual(f"{mw}, texte", m.get("text"))
            srcs = m.get("sources") or []
            if not srcs:
                err(mw, "aucune source")
            for k, s in enumerate(srcs):
                check_source(f"{mw}, source {k + 1}", s)
            if p.get("status") == "publié" and m.get("confidence") != "confirmé" and j == 0:
                err(mw, "un projet publié doit avoir un dernier jalon confirmé")
        dates = [str(m.get("date") or "") for m in ms]
        if dates != sorted(dates, reverse=True):
            err(w, "jalons à classer du plus récent au plus ancien")
    return seen


def check_briefs(projects):
    folder = ROOT / "data" / "briefs"
    if not folder.exists():
        return
    numbers = set()
    for path in sorted(folder.glob("*.json")):
        w = f"brief {path.name}"
        try:
            b = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            err(w, f"JSON invalide ({e})")
            continue
        if b.get("date") != path.stem:
            err(w, "le champ date doit correspondre au nom du fichier")
        if b.get("number") in numbers:
            err(w, "numéro en double")
        numbers.add(b.get("number"))
        for i, item in enumerate(b.get("moved") or []):
            if item.get("project_id") not in projects:
                err(w, f"projet inconnu « {item.get('project_id')} »")
            bilingual(f"{w}, ligne {i + 1}", item.get("line"))
        if b.get("deal"):
            if b["deal"].get("project_id") and b["deal"]["project_id"] not in projects:
                err(w, "projet du deal inconnu")
            bilingual(f"{w}, deal titre", b["deal"].get("title"))
            bilingual(f"{w}, deal texte", b["deal"].get("body"))
        if b.get("analysis"):
            bilingual(f"{w}, décryptage titre", b["analysis"].get("title"))
            bilingual(f"{w}, décryptage texte", b["analysis"].get("body"))


SOURCE_STATUSES = {"actif", "à vérifier", "référence"}
WEB_CHECKS = {"ok", "à confirmer", "injoignable"}
X_HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")
LINKEDIN_RE = re.compile(r"^https://www\.linkedin\.com/(company|school|showcase|in)/[^/\s]+$")


def check_sources(countries):
    """Contrôle le registre des sources officielles (data/sources.json)."""
    path = ROOT / "data" / "sources.json"
    try:
        sources = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        err("data/sources.json", "fichier manquant")
        return []
    except json.JSONDecodeError as e:
        err("data/sources.json", f"JSON invalide ({e})")
        return []
    seen_ids, seen_x = set(), {}
    extra_codes = {"AF", "INT", "EU", "US", "GB", "FR", "DE", "NL", "NO", "JP", "AE", "SA", "KW"}
    for i, s in enumerate(sources):
        sid = s.get("id") or f"#{i}"
        w = f"source {sid}"
        if not ID_RE.match(str(s.get("id") or "")):
            err(w, "identifiant invalide (minuscules et tirets)")
        if sid in seen_ids:
            err(w, "identifiant en double")
        seen_ids.add(sid)
        if not s.get("name"):
            err(w, "nom manquant")
        for code in str(s.get("country") or "").split(","):
            if code.strip() not in countries and code.strip() not in extra_codes:
                err(w, f"code pays inconnu « {code} »")
        if s.get("tier") != "A":
            err(w, "le registre ne contient que des sources de rang A")
        if s.get("priority") not in (1, 2, 3):
            err(w, "priorité 1, 2 ou 3 attendue")
        if s.get("status") not in SOURCE_STATUSES:
            err(w, f"statut inconnu « {s.get('status')} »")
        if s.get("web") and not str(s["web"]).startswith("https://"):
            err(w, "adresse web en https:// attendue")
        if s.get("web_check") is not None and s.get("web_check") not in WEB_CHECKS:
            err(w, f"état du site inconnu « {s.get('web_check')} »")
        x = s.get("x")
        if x:
            if not X_HANDLE_RE.match(x):
                err(w, f"identifiant X invalide « {x} » (sans @ ni lien)")
            if x.lower() in seen_x:
                err(w, f"compte X déjà attribué à {seen_x[x.lower()]}")
            seen_x[x.lower()] = sid
        if s.get("linkedin") and not LINKEDIN_RE.match(s["linkedin"]):
            err(w, "page LinkedIn au format https://www.linkedin.com/company/… attendue")
        if (x or s.get("linkedin")) and not s.get("social_check"):
            err(w, "compte social sans trace de vérification (social_check)")
        if s.get("status") == "actif" and not (s.get("web") or x or s.get("linkedin") or s.get("data")):
            err(w, "source active sans aucun canal de collecte")
        if s.get("data") and not str(s["data"].get("url") or "").startswith("https://"):
            err(w, "adresse de la base de données invalide")
    return sources


def main():
    countries = json.loads((ROOT / "site" / "countries.json").read_text(encoding="utf-8"))
    projects = check_projects(countries)
    check_briefs(projects)
    sources = check_sources(countries)
    if errors:
        print(f"{len(errors)} erreur(s) :")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK : {len(projects)} projets valides, {len(sources)} sources au registre.")


if __name__ == "__main__":
    main()
