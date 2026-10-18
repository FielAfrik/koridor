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


def main():
    countries = json.loads((ROOT / "site" / "countries.json").read_text(encoding="utf-8"))
    projects = check_projects(countries)
    check_briefs(projects)
    if errors:
        print(f"{len(errors)} erreur(s) :")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print(f"OK : {len(projects)} projets valides.")


if __name__ == "__main__":
    main()
