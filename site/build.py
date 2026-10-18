"""Générateur du site Koridor.

Lit data/projects.json et data/briefs/*.json, écrit le site statique bilingue dans dist/.
Usage : python3 site/build.py        (BASE_PATH=/nom-du-depot pour GitHub Pages)
Aucune dépendance hors bibliothèque standard.
"""
import html
import json
import os
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DIST = ROOT / "dist"

CONFIG = json.loads((SITE / "config.json").read_text(encoding="utf-8"))
COUNTRIES = json.loads((SITE / "countries.json").read_text(encoding="utf-8"))
BASE = os.environ.get("BASE_PATH", CONFIG.get("base_path", "")).rstrip("/")
NAME = CONFIG["site_name"]

LANGS = ("fr", "en")
OTHER = {"fr": "en", "en": "fr"}

T = {
    "fr": {
        "tagline": "Infrastructures · Énergie · Afrique",
        "hero": "L'Afrique qui se construit, suivie projet par projet.",
        "hero_sub": "Chaque semaine : quels projets avancent, qui les finance, qui les construit, et ce que ça change.",
        "cta": "Recevoir le Brief du lundi",
        "nav_projects": "Projets", "nav_brief": "Brief du lundi", "nav_method": "Méthode",
        "pipeline": "Le pipeline suivi, par stade",
        "projects_count": "{n} projets suivis · mis à jour le {d}",
        "all": "Tous",
        "sectors": {"energie": "Énergie", "transport": "Transport", "eau": "Eau", "numerique": "Villes & numérique"},
        "stages": ["Identification", "Faisabilité", "Financement", "Construction", "Exploitation"],
        "search": "Projet, pays, entreprise…", "search_label": "Rechercher un projet",
        "country_filter": "Pays", "all_countries": "Tous les pays",
        "filter_sector": "Filtrer par secteur",
        "view": "Voir la fiche", "stage": "Stade", "source": "Source", "sources": "Sources",
        "no_result": "Aucun projet ne correspond à ces filtres.",
        "unverified": "À confirmer",
        "unverified_banner": "Phase de lancement : les fiches marquées « À confirmer » sont en cours de vérification par notre équipe. Elles s'appuient sur une seule source de presse.",
        "back": "← Tous les projets",
        "updated": "Mis à jour le",
        "facts": "Fiche technique et financière",
        "f_country": "Pays", "f_sector": "Secteur", "f_stage": "Stade", "f_capacity": "Capacité",
        "f_cost": "Montant", "f_owner": "Maître d'ouvrage / sponsors", "f_lenders": "Bailleurs",
        "f_contractors": "EPC / entreprises", "f_target": "Mise en service visée",
        "unknown": "Non communiqué",
        "milestones": "Historique des jalons",
        "confirmed": "Confirmé",
        "same_sector": "Même secteur",
        "brief_title": "Le Brief du lundi",
        "brief_pitch": "Les projets d'infrastructure et d'énergie qui ont bougé en Afrique cette semaine, lus par un ingénieur. Cinq minutes, chaque lundi matin.",
        "brief_side": "10 projets qui ont bougé, 1 deal, 1 décryptage. Chaque lundi.",
        "subscribe": "S'abonner gratuitement",
        "subscribe_soon": "Inscription bientôt ouverte.",
        "email": "Adresse e-mail professionnelle",
        "archive": "Numéros précédents",
        "no_brief": "Le premier numéro paraîtra très bientôt.",
        "issue": "N° {n} · {d}",
        "moved": "Les projets qui ont bougé", "deal": "Le deal de la semaine", "analysis": "Le décryptage",
        "analysis_tag": "Analyse",
        "by_country": "Entrée par pays",
        "method_title": "Notre méthode",
        "footer": "Un média indépendant sur les projets d'infrastructure et d'énergie en Afrique.",
        "lang_switch": "English",
        "projects_slug": "projets", "brief_slug": "brief", "method_slug": "methode",
        "currency": {"USD": "dollars", "EUR": "euros", "XOF": "francs CFA", "XAF": "francs CFA", None: ""},
        "units": {"millions": "millions", "milliards": "milliards"},
    },
    "en": {
        "tagline": "Infrastructure · Energy · Africa",
        "hero": "Africa under construction, tracked project by project.",
        "hero_sub": "Every week: which projects are moving, who funds them, who builds them, and what they change.",
        "cta": "Get the Monday Brief",
        "nav_projects": "Projects", "nav_brief": "Monday Brief", "nav_method": "Method",
        "pipeline": "The pipeline we track, by stage",
        "projects_count": "{n} projects tracked · updated {d}",
        "all": "All",
        "sectors": {"energie": "Energy", "transport": "Transport", "eau": "Water", "numerique": "Cities & digital"},
        "stages": ["Identification", "Feasibility", "Financing", "Construction", "Operation"],
        "search": "Project, country, company…", "search_label": "Search projects",
        "country_filter": "Country", "all_countries": "All countries",
        "filter_sector": "Filter by sector",
        "view": "View project", "stage": "Stage", "source": "Source", "sources": "Sources",
        "no_result": "No project matches these filters.",
        "unverified": "To be confirmed",
        "unverified_banner": "Launch phase: entries marked \"To be confirmed\" are being checked by our team. They rely on a single press source.",
        "back": "← All projects",
        "updated": "Updated",
        "facts": "Technical and financial profile",
        "f_country": "Country", "f_sector": "Sector", "f_stage": "Stage", "f_capacity": "Capacity",
        "f_cost": "Amount", "f_owner": "Owner / sponsors", "f_lenders": "Lenders",
        "f_contractors": "EPC / contractors", "f_target": "Target commissioning",
        "unknown": "Not disclosed",
        "milestones": "Milestones",
        "confirmed": "Confirmed",
        "same_sector": "Same sector",
        "brief_title": "The Monday Brief",
        "brief_pitch": "The African infrastructure and energy projects that moved this week, read by an engineer. Five minutes, every Monday morning.",
        "brief_side": "10 projects that moved, 1 deal, 1 analysis. Every Monday.",
        "subscribe": "Subscribe for free",
        "subscribe_soon": "Sign-up opens soon.",
        "email": "Work email address",
        "archive": "Past issues",
        "no_brief": "The first issue is coming very soon.",
        "issue": "No. {n} · {d}",
        "moved": "Projects that moved", "deal": "Deal of the week", "analysis": "The analysis",
        "analysis_tag": "Analysis",
        "by_country": "Browse by country",
        "method_title": "Our method",
        "footer": "An independent outlet on infrastructure and energy projects in Africa.",
        "lang_switch": "Français",
        "projects_slug": "projects", "brief_slug": "brief", "method_slug": "method",
        "currency": {"USD": "dollars", "EUR": "euros", "XOF": "CFA francs", "XAF": "CFA francs", None: ""},
        "units": {"millions": "million", "milliards": "billion"},
    },
}

MONTHS = {
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
           "septembre", "octobre", "novembre", "décembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}

METHOD = {
    "fr": """
<p class="lead">Chaque fait publié ici est daté, sourcé et vérifié. Voici comment.</p>
<h2>Une équipe, un processus</h2>
<p>Chaque semaine, une équipe d'agents spécialisés repère les nouvelles sur les projets, les vérifie, met à jour la base, rédige en français et en anglais, puis relit. Le rédacteur en chef valide tout avant publication.</p>
<h2>Quand un fait est-il confirmé ?</h2>
<p>Un fait est confirmé s'il est publié par une source primaire (porteur du projet, bailleur, État, régulateur), ou par deux médias spécialisés indépendants. Sinon, il est marqué « À confirmer ».</p>
<h2>Les cinq stades d'un projet</h2>
<ol class="stages-def">
<li><strong>Identification</strong> : le projet est annoncé ou inscrit dans un plan.</li>
<li><strong>Faisabilité</strong> : études, appel d'offres, choix du partenaire.</li>
<li><strong>Financement</strong> : accords de prêt signés, bouclage financier.</li>
<li><strong>Construction</strong> : ordre de service ou début des travaux.</li>
<li><strong>Exploitation</strong> : mise en service, même partielle.</li>
</ol>
<h2>Chiffres</h2>
<p>Les montants sont repris tels qu'annoncés, dans leur devise d'origine, sans conversion ni arrondi.</p>
<h2>Corrections</h2>
<p>Une erreur publiée est corrigée et la correction est datée sur la page concernée.</p>
""",
    "en": """
<p class="lead">Every fact published here is dated, sourced and checked. Here is how.</p>
<h2>One team, one process</h2>
<p>Every week, a team of specialised agents spots project news, checks it, updates the database, writes in French and English, then edits. The editor-in-chief approves everything before publication.</p>
<h2>When is a fact confirmed?</h2>
<p>A fact is confirmed when a primary source publishes it (project owner, lender, government, regulator), or two independent specialist outlets do. Otherwise it is marked "To be confirmed".</p>
<h2>The five stages of a project</h2>
<ol class="stages-def">
<li><strong>Identification</strong>: the project is announced or listed in a plan.</li>
<li><strong>Feasibility</strong>: studies, tender, partner selection.</li>
<li><strong>Financing</strong>: loan agreements signed, financial close.</li>
<li><strong>Construction</strong>: notice to proceed or start of works.</li>
<li><strong>Operation</strong>: commissioning, even partial.</li>
</ol>
<h2>Figures</h2>
<p>Amounts are given as announced, in their original currency, without conversion or rounding.</p>
<h2>Corrections</h2>
<p>A published error is corrected, and the correction is dated on the page concerned.</p>
""",
}


def e(s):
    return html.escape(str(s), quote=True)


def fmt_date(d, lang):
    if not d:
        return ""
    parts = str(d).split("-")
    y, m = parts[0], int(parts[1])
    month = MONTHS[lang][m - 1]
    if len(parts) == 3:
        day = int(parts[2])
        if lang == "fr":
            return f"{'1er' if day == 1 else day} {month} {y}"
        return f"{day} {month} {y}"
    return f"{month} {y}" if lang == "fr" else f"{month} {y}"


def country_name(code_str, lang):
    i = 0 if lang == "fr" else 1
    return " / ".join(COUNTRIES[c.strip()][i] for c in str(code_str).split(","))


def fmt_cost(cost, lang):
    if not cost:
        return None
    t = T[lang]
    amount = cost["amount"]
    num = f"{amount:g}".replace(".", ",") if lang == "fr" else f"{amount:g}"
    unit = t["units"].get(cost.get("unit"), cost.get("unit") or "")
    cur = t["currency"].get(cost.get("currency"), cost.get("currency") or "")
    if lang == "fr" and cur:
        text = f"{num} {unit} d'{cur}" if cur[0] in "aeiou" else f"{num} {unit} de {cur}"
    else:
        text = f"{num} {unit} {cur}".strip()
    note = (cost.get("note") or {}).get(lang)
    return f"{text} — {note}" if note else text


def url(lang, *parts):
    path = "/".join([lang] + [p for p in parts if p])
    return f"{BASE}/{path}/"


def visible(projects):
    allowed = {"publié"} | ({"à vérifier"} if CONFIG.get("show_unverified") else set())
    return [p for p in projects if p["status"] in allowed]


def stage_bar(stage, lang, large=False):
    labels = T[lang]["stages"]
    cells = []
    for i, label in enumerate(labels):
        cls = "seg"
        if i < stage:
            cls += " done"
        elif i == stage:
            cls += " current"
        lab = f'<span class="seg-label">{e(label)}</span>' if large else ""
        cells.append(f'<div class="{cls}"><span class="seg-bar"></span>{lab}</div>')
    aria = f'{T[lang]["stage"]} {stage + 1}/5 : {labels[stage]}'
    return f'<div class="stagebar{" lg" if large else ""}" role="img" aria-label="{e(aria)}">{"".join(cells)}</div>'


def page(lang, title, body, path_parts, description=""):
    t = T[lang]
    other = OTHER[lang]
    other_parts = translate_path(path_parts, lang)
    full_title = f"{title} — {NAME}" if title != NAME else NAME
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description or t['hero_sub'])}">
<link rel="alternate" hreflang="{other}" href="{url(other, *other_parts)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;700;800&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{BASE}/assets/style.css">
</head>
<body>
<a class="skip" href="#contenu">{'Aller au contenu' if lang == 'fr' else 'Skip to content'}</a>
<header class="top">
<div class="wrap top-in">
<a class="brand" href="{url(lang)}">
<svg width="28" height="28" viewBox="0 0 28 28" aria-hidden="true"><rect x="2" y="16" width="5" height="10" fill="#E07A45"/><rect x="9" y="10" width="5" height="16" fill="#E07A45"/><rect x="16" y="4" width="5" height="22" fill="#fff"/><line x1="0" y1="27" x2="28" y2="27" stroke="#fff" stroke-width="2"/></svg>
<span>{e(NAME)}</span></a>
<nav aria-label="{'Navigation principale' if lang == 'fr' else 'Main navigation'}">
<a href="{url(lang)}">{e(t['nav_projects'])}</a>
<a href="{url(lang, t['brief_slug'])}">{e(t['nav_brief'])}</a>
<a href="{url(lang, t['method_slug'])}">{e(t['nav_method'])}</a>
<a class="lang" href="{url(other, *other_parts)}" hreflang="{other}" lang="{other}">{e(t['lang_switch'])}</a>
</nav>
</div>
</header>
<main id="contenu">
{body}
</main>
<footer class="foot">
<div class="wrap foot-in">
<span><strong>{e(NAME)}</strong> — {e(t['footer'])}</span>
<a href="{url(lang, t['method_slug'])}">{e(t['method_title'])}</a>
</div>
</footer>
</body>
</html>
"""


def translate_path(parts, lang):
    """Équivalent d'un chemin dans l'autre langue."""
    other = OTHER[lang]
    mapping = {T[lang][k]: T[other][k] for k in ("projects_slug", "brief_slug", "method_slug")}
    return [mapping.get(p, p) for p in parts]


def card(p, lang):
    t = T[lang]
    latest = p["milestones"][0]
    src = latest["sources"][0]
    badge = f'<span class="badge">{e(t["unverified"])}</span>' if p["status"] != "publié" else ""
    search_text = " ".join([p["name"][lang], country_name(p["country"], lang), " ".join(p.get("owner") or []),
                            " ".join(p.get("lenders") or []), " ".join(p.get("contractors") or [])]).lower()
    return f"""<article class="card" data-sector="{e(p['sector'])}" data-country="{e(p['country'])}" data-text="{e(search_text)}">
<div class="meta"><span class="strong">{e(country_name(p['country'], lang))}</span><span>{e(t['sectors'][p['sector']])}</span><span>{e(fmt_date(latest['date'], lang))}</span>{badge}</div>
<h3><a href="{url(lang, t['projects_slug'], p['id'])}">{e(p['name'][lang])}</a></h3>
<p>{e(latest['text'][lang])}</p>
{stage_bar(p['stage'], lang)}
<div class="card-foot"><span>{e(t['stage'])} : <strong>{e(t['stages'][p['stage']])}</strong> · {e(t['source'])} : {e(src['publisher'])}</span>
<a class="btn-outline" href="{url(lang, t['projects_slug'], p['id'])}">{e(t['view'])}</a></div>
</article>"""


def newsletter_box(lang, compact=False):
    t = T[lang]
    signup = CONFIG.get("newsletter_signup_url")
    if signup:
        action = f'<form class="signup" action="{e(signup)}" method="post" target="_blank"><label for="email-{"c" if compact else "f"}">{e(t["email"])}</label><input id="email-{"c" if compact else "f"}" type="email" name="email" required><button type="submit">{e(t["subscribe"])}</button></form>'
    else:
        action = f'<p class="soon">{e(t["subscribe_soon"])}</p>'
    return action


def build_home(lang, projects, briefs, updated):
    t = T[lang]
    vis = sorted(visible(projects), key=lambda p: p["milestones"][0]["date"], reverse=True)
    counts = [sum(1 for p in vis if p["stage"] == i) for i in range(5)]
    mx = max(counts) or 1
    stages_html = "".join(
        f'<div class="stat"><div class="stat-n">{c}</div><div class="stat-l">{e(t["stages"][i])}</div>'
        f'<div class="stat-track"><span style="width:{round(c / mx * 100)}%"></span></div></div>'
        for i, c in enumerate(counts))
    pills = [f'<button type="button" class="pill" aria-pressed="true" data-sector="">{e(t["all"])}</button>']
    for key, label in t["sectors"].items():
        if any(p["sector"] == key for p in vis):
            pills.append(f'<button type="button" class="pill" aria-pressed="false" data-sector="{key}">{e(label)}</button>')
    codes = sorted({c.strip() for p in vis for c in p["country"].split(",")}, key=lambda c: country_name(c, lang))
    options = "".join(f'<option value="{c}">{e(country_name(c, lang))}</option>' for c in codes)
    chips = "".join(f'<button type="button" class="chip" data-country="{c}">{e(country_name(c, lang))}</button>' for c in codes)
    banner = ""
    if any(p["status"] != "publié" for p in vis):
        banner = f'<p class="notice">{e(t["unverified_banner"])}</p>'
    cards = "\n".join(card(p, lang) for p in vis)
    latest_brief = ""
    if briefs:
        b = briefs[0]
        latest_brief = f'<p class="side-link"><a href="{url(lang, t["brief_slug"], b["date"])}">{e(t["issue"].format(n=b["number"], d=fmt_date(b["date"], lang)))} →</a></p>'
    body = f"""
<section class="hero"><div class="wrap hero-in">
<div><p class="kicker">{e(t['tagline'])}</p><h1>{e(t['hero'])}</h1><p class="sub">{e(t['hero_sub'])}</p></div>
<a class="btn" href="{url(lang, t['brief_slug'])}">{e(t['cta'])}</a>
</div></section>
<section class="wrap pipeline" aria-labelledby="pl">
<div class="row-head"><h2 id="pl">{e(t['pipeline'])}</h2><span class="mono">{e(t['projects_count'].format(n=len(vis), d=fmt_date(updated, lang)))}</span></div>
<div class="stats">{stages_html}</div>
</section>
<div class="wrap layout">
<div class="col-main">
{banner}
<div class="filters">
<div class="pills" role="group" aria-label="{e(t['filter_sector'])}">{''.join(pills)}</div>
<div class="filter-row">
<label class="search"><span class="sr">{e(t['search_label'])}</span><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="7" cy="7" r="5"/><line x1="11" y1="11" x2="15" y2="15"/></svg><input type="search" id="q" placeholder="{e(t['search'])}"></label>
<label class="select"><span class="sr">{e(t['country_filter'])}</span><select id="country"><option value="">{e(t['all_countries'])}</option>{options}</select></label>
</div>
</div>
<div class="cards" id="cards">
{cards}
</div>
<p class="empty" id="empty" hidden>{e(t['no_result'])}</p>
</div>
<aside class="col-side">
<section class="box dark"><h2>{e(t['brief_title'])}</h2><p>{e(t['brief_side'])}</p>{latest_brief}<a class="btn btn-block" href="{url(lang, t['brief_slug'])}">{e(t['subscribe'])}</a></section>
<section class="box"><h2>{e(t['by_country'])}</h2><div class="chips">{chips}</div></section>
</aside>
</div>
<script>
(function(){{
  var pills=[].slice.call(document.querySelectorAll('.pill')),cards=[].slice.call(document.querySelectorAll('#cards .card'));
  var q=document.getElementById('q'),sel=document.getElementById('country'),empty=document.getElementById('empty'),sector='';
  function apply(){{
    var term=(q.value||'').toLowerCase().trim(),c=sel.value,n=0;
    cards.forEach(function(el){{
      var ok=(!sector||el.dataset.sector===sector)&&(!c||el.dataset.country.split(',').indexOf(c)>-1)&&(!term||el.dataset.text.indexOf(term)>-1);
      el.hidden=!ok; if(ok)n++;
    }});
    empty.hidden=n>0;
  }}
  pills.forEach(function(b){{b.addEventListener('click',function(){{sector=b.dataset.sector;pills.forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false');}});apply();}});}});
  [].slice.call(document.querySelectorAll('.chip')).forEach(function(b){{b.addEventListener('click',function(){{sel.value=b.dataset.country;apply();document.getElementById('cards').scrollIntoView({{behavior:'smooth'}});}});}});
  q.addEventListener('input',apply);sel.addEventListener('change',apply);
}})();
</script>
"""
    return page(lang, NAME, body, [])


def build_project(lang, p, projects):
    t = T[lang]
    joined = lambda xs: ", ".join(xs) if xs else None
    rows = [
        (t["f_country"], country_name(p["country"], lang)),
        (t["f_sector"], t["sectors"][p["sector"]]),
        (t["f_stage"], t["stages"][p["stage"]]),
        (t["f_capacity"], p.get("capacity")),
        (t["f_cost"], fmt_cost(p.get("cost"), lang)),
        (t["f_owner"], joined(p.get("owner"))),
        (t["f_lenders"], joined(p.get("lenders"))),
        (t["f_contractors"], joined(p.get("contractors"))),
        (t["f_target"], p.get("target_date")),
    ]
    muted_cls = ' class="muted"'
    table = "".join(
        f'<tr><th scope="row">{e(k)}</th><td{"" if v else muted_cls}>{e(v or t["unknown"])}</td></tr>'
        for k, v in rows)
    ms_html = []
    for m in p["milestones"]:
        srcs = " · ".join(
            f'<a href="{e(s["url"])}" rel="noopener" target="_blank">{e(s["publisher"])}</a>' for s in m["sources"])
        conf = t["confirmed"] if m["confidence"] == "confirmé" else t["unverified"]
        cls = "ok" if m["confidence"] == "confirmé" else "tbc"
        ms_html.append(
            f'<li><span class="dot {cls}"></span><div class="mono">{e(fmt_date(m["date"], lang))} · <span class="conf {cls}">{e(conf)}</span></div>'
            f'<p>{e(m["text"][lang])}</p><div class="src">{e(t["sources"])} : {srcs}</div></li>')
    related = [r for r in visible(projects) if r["sector"] == p["sector"] and r["id"] != p["id"]][:4]
    rel_html = "".join(
        f'<li><a href="{url(lang, t["projects_slug"], r["id"])}"><strong>{e(r["name"][lang])}</strong>'
        f'<span>{e(country_name(r["country"], lang))} · {e(t["stages"][r["stage"]])}</span></a></li>' for r in related)
    badge = f'<span class="badge">{e(t["unverified"])}</span>' if p["status"] != "publié" else ""
    body = f"""
<div class="wrap project">
<a class="back" href="{url(lang)}">{e(t['back'])}</a>
<div class="meta"><span class="strong">{e(country_name(p['country'], lang))}</span><span>{e(t['sectors'][p['sector']])}</span><span>{e(t['updated'])} {e(fmt_date(p['updated'], lang))}</span>{badge}</div>
<h1>{e(p['name'][lang])}</h1>
<p class="sub">{e(p['summary'][lang])}</p>
<section class="box stage-box" aria-label="{e(t['stage'])}">{stage_bar(p['stage'], lang, large=True)}</section>
<div class="layout">
<div class="col-main">
<section class="box"><h2>{e(t['facts'])}</h2><div class="table-scroll"><table class="facts">{table}</table></div></section>
<section class="box"><h2>{e(t['milestones'])}</h2><ol class="timeline">{''.join(ms_html)}</ol></section>
</div>
<aside class="col-side">
<section class="box dark"><h2>{e(t['brief_title'])}</h2><p>{e(t['brief_side'])}</p><a class="btn btn-block" href="{url(lang, t['brief_slug'])}">{e(t['subscribe'])}</a></section>
{f'<section class="box"><h2>{e(t["same_sector"])}</h2><ul class="related">{rel_html}</ul></section>' if rel_html else ''}
</aside>
</div>
</div>"""
    return page(lang, p["name"][lang], body, [t["projects_slug"], p["id"]], p["summary"][lang])


def paragraphs(text):
    return "".join(f"<p>{e(par.strip())}</p>" for par in str(text).split("\n\n") if par.strip())


def build_brief_issue(lang, b, by_id):
    t = T[lang]
    moved = "".join(
        f'<li><a href="{url(lang, t["projects_slug"], m["project_id"])}"><strong>{e(country_name(by_id[m["project_id"]]["country"], lang))}</strong></a> — {e(m["line"][lang])}</li>'
        for m in b.get("moved") or [])
    deal = ""
    if b.get("deal"):
        deal = f'<h2>{e(t["deal"])}</h2><h3>{e(b["deal"]["title"][lang])}</h3>{paragraphs(b["deal"]["body"][lang])}'
    analysis = ""
    if b.get("analysis"):
        analysis = (f'<h2>{e(t["analysis"])}</h2><p class="tag">{e(t["analysis_tag"])}</p>'
                    f'<h3>{e(b["analysis"]["title"][lang])}</h3>{paragraphs(b["analysis"]["body"][lang])}')
    title = f'{t["brief_title"]} — {t["issue"].format(n=b["number"], d=fmt_date(b["date"], lang))}'
    body = f"""
<div class="wrap narrow issue">
<a class="back" href="{url(lang, t['brief_slug'])}">← {e(t['brief_title'])}</a>
<p class="kicker">{e(t['issue'].format(n=b['number'], d=fmt_date(b['date'], lang)))}</p>
<h1>{e(t['brief_title'])}</h1>
<h2>{e(t['moved'])}</h2><ol class="moved">{moved}</ol>
{deal}
{analysis}
</div>"""
    return page(lang, title, body, [t["brief_slug"], b["date"]])


def build_brief_index(lang, briefs):
    t = T[lang]
    items = "".join(
        f'<li><a href="{url(lang, t["brief_slug"], b["date"])}">{e(t["issue"].format(n=b["number"], d=fmt_date(b["date"], lang)))}</a></li>'
        for b in briefs)
    archive = f'<ul class="archive">{items}</ul>' if items else f'<p class="muted">{e(t["no_brief"])}</p>'
    body = f"""
<div class="wrap narrow">
<p class="kicker">{'Newsletter hebdomadaire · gratuite' if lang == 'fr' else 'Weekly newsletter · free'}</p>
<h1>{e(t['brief_title'])}</h1>
<p class="sub">{e(t['brief_pitch'])}</p>
<div class="box">{newsletter_box(lang)}</div>
<h2>{e(t['archive'])}</h2>
{archive}
</div>"""
    return page(lang, t["brief_title"], body, [t["brief_slug"]])


def build_method(lang):
    t = T[lang]
    body = f'<div class="wrap narrow prose"><h1>{e(t["method_title"])}</h1>{METHOD[lang]}</div>'
    return page(lang, t["method_title"], body, [t["method_slug"]])


def write(rel, content):
    path = DIST / rel / "index.html" if not rel.endswith(".html") else DIST / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main():
    projects = json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in projects}
    brief_dir = ROOT / "data" / "briefs"
    briefs = sorted(
        (json.loads(f.read_text(encoding="utf-8")) for f in brief_dir.glob("*.json")) if brief_dir.exists() else [],
        key=lambda b: b["date"], reverse=True)
    updated = max((p["updated"] for p in projects), default=date.today().isoformat())

    if DIST.exists():
        shutil.rmtree(DIST)
    (DIST / "assets").mkdir(parents=True)
    shutil.copy(SITE / "style.css", DIST / "assets" / "style.css")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    (DIST / "index.html").write_text(
        f'<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>{e(NAME)}</title>'
        f'<meta http-equiv="refresh" content="0; url={BASE}/fr/"></head>'
        f'<body><a href="{BASE}/fr/">{e(NAME)}</a></body></html>', encoding="utf-8")

    pages = 0
    for lang in LANGS:
        t = T[lang]
        write(lang, build_home(lang, projects, briefs, updated))
        write(f"{lang}/{t['brief_slug']}", build_brief_index(lang, briefs))
        write(f"{lang}/{t['method_slug']}", build_method(lang))
        pages += 3
        for p in visible(projects):
            write(f"{lang}/{t['projects_slug']}/{p['id']}", build_project(lang, p, projects))
            pages += 1
        for b in briefs:
            write(f"{lang}/{t['brief_slug']}/{b['date']}", build_brief_issue(lang, b, by_id))
            pages += 1
    print(f"Site généré : {pages} pages dans dist/")


if __name__ == "__main__":
    main()
