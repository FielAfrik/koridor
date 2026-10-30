"""Générateur du site Koridor.

Lit data/projects.json et data/briefs/*.json, écrit le site statique bilingue dans dist/.
Usage : python3 site/build.py        (BASE_PATH=/nom-du-depot pour GitHub Pages)
Aucune dépendance hors bibliothèque standard.
La carte (site/africa.json) se régénère avec scripts/carte/make.mjs si besoin.
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
AFRICA = json.loads((SITE / "africa.json").read_text(encoding="utf-8"))
BASE = os.environ.get("BASE_PATH", CONFIG.get("base_path", "")).rstrip("/")
NAME = CONFIG["site_name"]
# Adresse publique du site, pour les liens absolus des aperçus de partage et du plan du site.
ORIGIN = CONFIG.get("site_origin", "").rstrip("/")
SITEMAP = []

# Mesure d'audience (Umami, sans cookie). Rien n'est injecté tant que website_id est vide.
ANALYTICS = CONFIG.get("analytics") or {}
TRACKING = bool(ANALYTICS.get("website_id"))


def tracking_tags():
    if not TRACKING:
        return ""
    domains = ANALYTICS.get("domains")
    dom = f' data-domains="{html.escape(domains, quote=True)}"' if domains else ""
    return (f'<script defer src="{html.escape(ANALYTICS.get("script_url", "https://cloud.umami.is/script.js"), quote=True)}" '
            f'data-website-id="{html.escape(ANALYTICS["website_id"], quote=True)}"{dom}></script>\n'
            f'<script defer src="{BASE}/assets/audience.js"></script>\n')

LANGS = ("fr", "en")
OTHER = {"fr": "en", "en": "fr"}

T = {
    "fr": {
        "signature": "Comprendre les infrastructures qui transforment l'Afrique.",
        "hero_sub": "Corridors, énergie, transport, eau et villes : quels projets avancent en Afrique, qui les finance, qui les construit, et ce que ça change.",
        "nav_projects": "Projets", "nav_brief": "Brief du lundi", "nav_method": "Méthode", "nav_about": "À propos",
        "featured": "À la une",
        "this_week": "Ce qui a bougé",
        "read_project": "Lire la fiche du projet",
        "pipeline": "Où en sont les projets suivis",
        "pipeline_sum": "{n} projets dans {c} pays, mis à jour le {d}.",
        "pipeline_note": "Chaque projet avance par cinq stades, de l'annonce à la mise en service.",
        "amounts": "Montants annoncés", "by_sector": "Par secteur",
        "amounts_note": "Tels qu'annoncés, sans conversion de devise.",
        "explore": "Tous les projets",
        "map_title": "Où se construisent-ils ?",
        "map_hint": "Touchez un pays pour filtrer la liste.",
        "map_label": "Carte des projets suivis par pays",
        "n_projects": {1: "1 projet", "n": "{n} projets"},
        "all": "Tous",
        "sectors": {"energie": "Énergie", "transport": "Transport & corridors", "eau": "Eau", "numerique": "Villes & numérique"},
        "stages": ["Identification", "Faisabilité", "Financement", "Construction", "Exploitation"],
        "search": "Projet, pays, entreprise, bailleur", "search_label": "Rechercher un projet",
        "country_filter": "Pays", "all_countries": "Tous les pays",
        "filter_sector": "Filtrer par secteur",
        "stage": "Stade", "sources": "Sources",
        "no_result": "Aucun projet ne correspond. Retirez un filtre ou changez de mot-clé.",
        "reset": "Effacer les filtres",
        "unverified": "À confirmer",
        "unverified_card": "Source unique, en cours de vérification",
        "unverified_banner": "Phase de lancement : les fiches « À confirmer » reposent sur une seule source de presse et sont en cours de vérification.",
        "back": "Tous les projets",
        "updated": "Mis à jour le",
        "facts": "Fiche technique et financière",
        "f_country": "Pays", "f_sector": "Secteur", "f_stage": "Stade", "f_capacity": "Capacité",
        "f_cost": "Montant", "f_owner": "Maître d'ouvrage et sponsors", "f_lenders": "Bailleurs",
        "f_contractors": "EPC et entreprises", "f_target": "Mise en service visée",
        "missing": "Pas encore rendu public : {x}.",
        "milestones": "Historique des jalons",
        "corrections": "Corrections",
        "confirmed": "Confirmé",
        "same_sector": "Dans le même secteur",
        "brief_title": "Le Brief du lundi",
        "brief_pitch": "Les projets d'infrastructure et d'énergie qui ont bougé en Afrique cette semaine, lus par un ingénieur. Cinq minutes, chaque lundi matin.",
        "brief_side": "Jusqu'à dix projets qui ont bougé, un deal, un décryptage. Chaque lundi, gratuit.",
        "subscribe": "Recevoir le Brief",
        "subscribe_soon": "Les inscriptions ouvrent très bientôt.",
        "email": "Adresse e-mail professionnelle",
        "archive": "Numéros précédents",
        "no_brief": "Le premier numéro paraîtra très bientôt.",
        "issue": "N° {n}, {d}",
        "moved": "Les projets qui ont bougé", "deal": "Le deal de la semaine", "analysis": "Le décryptage",
        "analysis_tag": "Analyse",
        "method_title": "Notre méthode",
        "about_title": "À propos de Koridor", "about_sub": "Comprendre les projets qui transforment l’Afrique",
        "footer": "Média indépendant sur les infrastructures, l'énergie et le développement durable en Afrique.",
        "privacy": "Mesure d'audience anonyme, sans cookie ni donnée personnelle.",
        "lang_switch": "English",
        "projects_slug": "projets", "brief_slug": "brief", "method_slug": "methode", "about_slug": "a-propos",
        "currency": {"USD": "dollars", "EUR": "euros", "XOF": "francs CFA", "XAF": "francs CFA", None: ""},
        "units": {"millions": "millions", "milliards": "milliards"},
        "skip": "Aller au contenu", "nav_label": "Navigation principale",
    },
    "en": {
        "signature": "Understanding the infrastructure transforming Africa.",
        "hero_sub": "Corridors, energy, transport, water and cities: which African projects are moving, who funds them, who builds them, and what they change.",
        "nav_projects": "Projects", "nav_brief": "Monday Brief", "nav_method": "Method", "nav_about": "About",
        "featured": "Top story",
        "this_week": "What moved",
        "read_project": "Read the project profile",
        "pipeline": "Where the tracked projects stand",
        "pipeline_sum": "{n} projects in {c} countries, updated {d}.",
        "pipeline_note": "Every project moves through five stages, from announcement to commissioning.",
        "amounts": "Announced amounts", "by_sector": "By sector",
        "amounts_note": "As announced, with no currency conversion.",
        "explore": "All projects",
        "map_title": "Where are they being built?",
        "map_hint": "Tap a country to filter the list.",
        "map_label": "Map of tracked projects by country",
        "n_projects": {1: "1 project", "n": "{n} projects"},
        "all": "All",
        "sectors": {"energie": "Energy", "transport": "Transport & corridors", "eau": "Water", "numerique": "Cities & digital"},
        "stages": ["Identification", "Feasibility", "Financing", "Construction", "Operation"],
        "search": "Project, country, company, lender", "search_label": "Search projects",
        "country_filter": "Country", "all_countries": "All countries",
        "filter_sector": "Filter by sector",
        "stage": "Stage", "sources": "Sources",
        "no_result": "No project matches. Remove a filter or try another keyword.",
        "reset": "Clear filters",
        "unverified": "To be confirmed",
        "unverified_card": "Single source, being checked",
        "unverified_banner": "Launch phase: entries marked \"To be confirmed\" rely on a single press source and are being checked.",
        "back": "All projects",
        "updated": "Updated",
        "facts": "Technical and financial profile",
        "f_country": "Country", "f_sector": "Sector", "f_stage": "Stage", "f_capacity": "Capacity",
        "f_cost": "Amount", "f_owner": "Owner and sponsors", "f_lenders": "Lenders",
        "f_contractors": "EPC and contractors", "f_target": "Target commissioning",
        "missing": "Not yet public: {x}.",
        "milestones": "Milestones",
        "corrections": "Corrections",
        "confirmed": "Confirmed",
        "same_sector": "In the same sector",
        "brief_title": "The Monday Brief",
        "brief_pitch": "The African infrastructure and energy projects that moved this week, read by an engineer. Five minutes, every Monday morning.",
        "brief_side": "Up to ten projects that moved, one deal, one analysis. Every Monday, free.",
        "subscribe": "Get the Brief",
        "subscribe_soon": "Sign-up opens very soon.",
        "email": "Work email address",
        "archive": "Past issues",
        "no_brief": "The first issue is coming very soon.",
        "issue": "No. {n}, {d}",
        "moved": "Projects that moved", "deal": "Deal of the week", "analysis": "The analysis",
        "analysis_tag": "Analysis",
        "method_title": "Our method",
        "about_title": "About Koridor", "about_sub": "Understanding the projects transforming Africa",
        "footer": "Independent outlet on infrastructure, energy and sustainable development in Africa.",
        "privacy": "Anonymous audience measurement, no cookies, no personal data.",
        "lang_switch": "Français",
        "projects_slug": "projects", "brief_slug": "brief", "method_slug": "method", "about_slug": "about",
        "currency": {"USD": "dollars", "EUR": "euros", "XOF": "CFA francs", "XAF": "CFA francs", None: ""},
        "units": {"millions": "million", "milliards": "billion"},
        "skip": "Skip to content", "nav_label": "Main navigation",
    },
}

MONTHS = {
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
           "septembre", "octobre", "novembre", "décembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}

ABOUT = {
    "fr": """
<p class="lead">Koridor est un média consacré aux infrastructures, à l’énergie et au développement durable en Afrique. Son nom vient des grands axes de développement, des corridors, ces axes qui relient les territoires, portent les échanges et dessinent l’économie du continent.</p>
<h2>Ce que nous faisons</h2>
<p>Nous suivons les projets un par un : centrales, réseaux électriques, corridors de transport, ports, eau, numérique. Pour chacun, une fiche indique où il en est, de l’identification à la mise en service, qui le porte, qui le finance et qui le construit. Chaque semaine, le Brief du lundi résume ce qui a bougé, et nos décryptages éclairent les enjeux techniques, économiques et environnementaux.</p>
<h2>Pour qui ?</h2>
<p>Pour celles et ceux qui financent, conçoivent, construisent ou décident : investisseurs, bailleurs, entreprises, administrations. Et pour tous ceux qui veulent comprendre comment se construit l’Afrique de demain.</p>
<h2>Notre méthode</h2>
<p>Chaque information est datée et rattachée à sa source. Un fait n’est confirmé que s’il émane du porteur du projet, d’un bailleur ou d’une autorité publique, ou de deux médias indépendants. Les chiffres sont repris tels qu’annoncés, et toute erreur est corrigée visiblement. Notre veille s’appuie sur des outils d’intelligence artificielle ; chaque contenu est vérifié et validé par la rédaction avant publication.</p>
<h2>Notre conviction</h2>
<p>Comprendre les infrastructures, c’est comprendre les choix qui façonnent l’avenir de nos sociétés. Un ouvrage ne vaut que par son utilité, sa durabilité et sa capacité à améliorer concrètement la vie des populations. C’est à cette aune que nous regardons chaque projet.</p>
<p class="closing"><strong>Koridor, les infrastructures qui transforment l’Afrique.</strong></p>
""",
    "en": """
<p class="lead">Koridor is a media outlet covering infrastructure, energy and sustainable development in Africa. Its name comes from the great development axes, the corridors: the routes that link territories, carry trade and shape the continent’s economy.</p>
<h2>What we do</h2>
<p>We track projects one by one: power plants, electricity grids, transport corridors, ports, water, digital. For each one, a profile shows where it stands, from identification to commissioning, who owns it, who funds it and who builds it. Every week, the Monday Brief sums up what moved, and our analyses shed light on the technical, economic and environmental stakes.</p>
<h2>Who is it for?</h2>
<p>For those who finance, design, build or decide: investors, lenders, companies, public administrations. And for anyone who wants to understand how tomorrow’s Africa is being built.</p>
<h2>Our method</h2>
<p>Every piece of information is dated and linked to its source. A fact is confirmed only when it comes from the project owner, a lender or a public authority, or from two independent media outlets. Figures are given as announced, and any error is visibly corrected. Our monitoring relies on artificial intelligence tools; every piece of content is checked and approved by the editorial team before publication.</p>
<h2>Our conviction</h2>
<p>Understanding infrastructure means understanding the choices that shape the future of our societies. A structure is only worth its usefulness, its durability and its ability to make a tangible difference to people’s lives. That is the yardstick we apply to every project.</p>
<p class="closing"><strong>Koridor, the infrastructure transforming Africa.</strong></p>
""",
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



ICONS = {
    "energie": '<path d="M9.5 1.5 3.5 9h4l-1 5.5 6-7.5h-4l1-5.5z"/>',
    "transport": '<path d="M5 1.5v13M11 1.5v13M5 4h6M5 8h6M5 12h6"/>',
    "eau": '<path d="M8 1.8S3.5 7 3.5 10a4.5 4.5 0 0 0 9 0C12.5 7 8 1.8 8 1.8z"/>',
    "numerique": '<circle cx="3.5" cy="8" r="2"/><circle cx="12.5" cy="3.5" r="2"/><circle cx="12.5" cy="12.5" r="2"/><path d="M5.3 7.1 10.7 4.4M5.3 8.9l5.4 2.7"/>',
}

LOGO = ('<svg class="logo" width="30" height="30" viewBox="0 0 30 30" aria-hidden="true">'
        '<path d="M8 3v24" stroke="currentColor" stroke-width="3.6" stroke-linecap="round"/>'
        '<path d="M8 15 25 4" stroke="#F2B705" stroke-width="3.6" stroke-linecap="round"/>'
        '<path d="M8 15 25 26" stroke="#2BB383" stroke-width="3.6" stroke-linecap="round"/>'
        '<circle cx="8" cy="15" r="4.2" fill="#0F1E2B" stroke="currentColor" stroke-width="2.4"/></svg>')

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3E"
           "%3Crect width='30' height='30' rx='6' fill='%230F1E2B'/%3E"
           "%3Cpath d='M9 5v20' stroke='%23fff' stroke-width='3.4' stroke-linecap='round'/%3E"
           "%3Cpath d='M9 15 24 6' stroke='%23F2B705' stroke-width='3.4' stroke-linecap='round'/%3E"
           "%3Cpath d='M9 15l15 9' stroke='%232BB383' stroke-width='3.4' stroke-linecap='round'/%3E%3C/svg%3E")


def lx(v, lang):
    """Valeur de champ factuel : texte neutre (nom propre, chiffre) ou objet {fr, en}."""
    if isinstance(v, dict):
        return v.get(lang) or v.get("fr")
    return v


def e(s):
    return html.escape(str(s), quote=True)


def icon(sector):
    return (f'<svg class="ico" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[sector]}</svg>')


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
    return f"{month} {y}"


def country_name(code_str, lang):
    i = 0 if lang == "fr" else 1
    return " / ".join(COUNTRIES[c.strip()][i] for c in str(code_str).split(","))


def codes_of(p):
    return [c.strip() for c in p["country"].split(",")]


def fmt_amount(cost, lang):
    """Montant seul (sans la note), tel qu'annoncé."""
    if not cost:
        return None
    t = T[lang]
    amount = cost["amount"]
    num = f"{amount:g}".replace(".", ",") if lang == "fr" else f"{amount:g}"
    unit = t["units"].get(cost.get("unit"), cost.get("unit") or "")
    cur = t["currency"].get(cost.get("currency"), cost.get("currency") or "")
    if lang == "fr" and cur:
        return f"{num} {unit} d'{cur}" if cur[0] in "aeiou" else f"{num} {unit} de {cur}"
    return f"{num} {unit} {cur}".strip()


def cost_note(cost, lang):
    return ((cost or {}).get("note") or {}).get(lang)


def fmt_cost(cost, lang):
    text = fmt_amount(cost, lang)
    if not text:
        return None
    note = cost_note(cost, lang)
    return f"{text} ({note[0].lower() + note[1:]})" if note else text


def plural(lang, n):
    forms = T[lang]["n_projects"]
    return forms[1] if n == 1 else forms["n"].format(n=n)


def url(lang, *parts):
    path = "/".join([lang] + [p for p in parts if p])
    return f"{BASE}/{path}/"


def visible(projects):
    allowed = {"publié"} | ({"à vérifier"} if CONFIG.get("show_unverified") else set())
    return [p for p in projects if p["status"] in allowed]


def route(stage, lang, size="sm", counts=None):
    """La ligne de corridor : cinq stations, du stade 0 (identification) au stade 4 (exploitation)."""
    labels = T[lang]["stages"]
    stops = []
    for i, label in enumerate(labels):
        state = "done" if stage is not None and i < stage else ("now" if i == stage else "next")
        if counts is not None:
            state = "on" if counts[i] else "off"
        num = f'<span class="stop-n">{counts[i]}</span>' if counts is not None else ""
        lab = f'<span class="stop-l">{e(label)}</span>' if size != "sm" else ""
        stops.append(f'<li class="stop {state}">{num}<span class="stop-dot"></span>{lab}</li>')
    if counts is not None:
        aria = " ; ".join(f"{labels[i]} : {c}" for i, c in enumerate(counts))
    else:
        aria = f'{T[lang]["stage"]} {stage + 1}/5 : {labels[stage]}'
    return f'<ol class="route route-{size}" role="img" aria-label="{e(aria)}">{"".join(stops)}</ol>'


def translate_path(parts, lang):
    other = OTHER[lang]
    keys = ("projects_slug", "brief_slug", "method_slug", "about_slug")
    mapping = {T[lang][k]: T[other][k] for k in keys}
    return [mapping.get(p, p) for p in parts]


def share_tags(lang, title, description, path_parts, other, other_parts, kind):
    """Balises d'aperçu (LinkedIn, WhatsApp, X, e-mail), lien canonique et plan du site."""
    if not ORIGIN:
        return ""
    here = ORIGIN + url(lang, *path_parts)
    SITEMAP.append(here)
    locale = {"fr": "fr_FR", "en": "en_GB"}
    image = f"{ORIGIN}{BASE}/assets/og-{lang}.png"
    return (f'<link rel="canonical" href="{e(here)}">\n'
            f'<link rel="alternate" hreflang="{lang}" href="{e(here)}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{e(ORIGIN + url("fr", *(path_parts if lang == "fr" else other_parts)))}">\n'
            f'<meta property="og:site_name" content="{e(NAME)}">\n'
            f'<meta property="og:type" content="{kind}">\n'
            f'<meta property="og:title" content="{e(title)}">\n'
            f'<meta property="og:description" content="{e(description)}">\n'
            f'<meta property="og:url" content="{e(here)}">\n'
            f'<meta property="og:image" content="{e(image)}">\n'
            f'<meta property="og:image:width" content="1200">\n'
            f'<meta property="og:image:height" content="630">\n'
            f'<meta property="og:locale" content="{locale[lang]}">\n'
            f'<meta property="og:locale:alternate" content="{locale[other]}">\n'
            f'<meta name="twitter:card" content="summary_large_image">\n')


def page(lang, title, body, path_parts, description="", current="", kind="website"):
    t = T[lang]
    other = OTHER[lang]
    other_parts = translate_path(path_parts, lang)
    if lang == "fr":
        # Espaces insécables de la typographie française
        for a, b in ((" :", "\u00a0:"), (" ;", "\u202f;"), (" ?", "\u202f?"), (" !", "\u202f!"),
                     ("« ", "«\u00a0"), (" »", "\u00a0»")):
            body = body.replace(a, b)
    full_title = f"{title} | {NAME}" if title != NAME else f"{NAME} | {t['signature'].rstrip('.')}"
    nav = []
    for key, slug in (("nav_projects", ""), ("nav_brief", t["brief_slug"]), ("nav_about", t["about_slug"])):
        cur = ' aria-current="page"' if current == key else ""
        nav.append(f'<a href="{url(lang, slug)}"{cur}>{e(t[key])}</a>')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title>
<meta name="description" content="{e(description or t['hero_sub'])}">
{share_tags(lang, title if title != NAME else full_title, description or t['hero_sub'], path_parts, other, other_parts, kind)}
<meta name="theme-color" content="#0F1E2B">
<link rel="icon" href="{FAVICON}">
<link rel="alternate" hreflang="{other}" href="{url(other, *other_parts)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&display=swap">
<link rel="stylesheet" href="{BASE}/assets/style.css">
{tracking_tags()}</head>
<body>
<a class="skip" href="#contenu">{e(t['skip'])}</a>
<header class="top">
<div class="wrap top-in">
<a class="brand" href="{url(lang)}">{LOGO}<span class="brand-name">{e(NAME)}</span></a>
<p class="brand-sig">{e(t['signature'])}</p>
<nav aria-label="{e(t['nav_label'])}">
{''.join(nav)}
<a class="lang" href="{url(other, *other_parts)}" hreflang="{other}" lang="{other}">{e(t['lang_switch'])}</a>
</nav>
</div>
</header>
<main id="contenu">
{body}
</main>
<footer class="foot">
<div class="wrap foot-in">
<div class="foot-brand"><a class="brand" href="{url(lang)}">{LOGO}<span class="brand-name">{e(NAME)}</span></a>
<p>{e(t['footer'])}</p>{f'<p class="fine">{e(t["privacy"])}</p>' if TRACKING else ''}</div>
<nav aria-label="{e(t['nav_label'])}">{''.join(nav)}</nav>
</div>
</footer>
</body>
</html>
"""


def card(p, lang):
    t = T[lang]
    latest = p["milestones"][0]
    link = url(lang, t["projects_slug"], p["id"])
    search_text = " ".join([p["name"][lang], country_name(p["country"], lang), t["sectors"][p["sector"]],
                            " ".join(lx(x, lang) for x in p.get("owner") or []),
                            " ".join(lx(x, lang) for x in p.get("lenders") or []),
                            " ".join(lx(x, lang) for x in p.get("contractors") or [])]).lower()
    amount = fmt_amount(p.get("cost"), lang)
    amount_html = ""
    if amount:
        note = cost_note(p.get("cost"), lang)
        amount_html = f'<p class="card-amount"><strong>{e(amount)}</strong>{f" <span>{e(note)}</span>" if note else ""}</p>'
    status = f'<p class="card-status">{e(t["unverified_card"])}</p>' if p["status"] != "publié" else ""
    return f"""<article class="card" data-sector="{e(p['sector'])}" data-country="{e(','.join(codes_of(p)))}" data-text="{e(search_text)}">
<div class="card-top"><span class="sector s-{e(p['sector'])}">{icon(p['sector'])}{e(t['sectors'][p['sector']])}</span><time datetime="{e(latest['date'])}">{e(fmt_date(latest['date'], lang))}</time></div>
<p class="card-country">{e(country_name(p['country'], lang))}</p>
<h3><a href="{link}">{e(p['name'][lang])}</a></h3>
<p class="card-text">{e(latest['text'][lang])}</p>
{amount_html}
<div class="card-stage">{route(p['stage'], lang)}<span>{e(t['stages'][p['stage']])}</span></div>
{status}
</article>"""


def newsletter_box(lang, compact=False):
    t = T[lang]
    signup = CONFIG.get("newsletter_signup_url")
    if signup:
        sid = "c" if compact else "f"
        return (f'<form class="signup" action="{e(signup)}" method="post" target="_blank">'
                f'<label for="email-{sid}">{e(t["email"])}</label><input id="email-{sid}" type="email" name="email" required>'
                f'<button class="btn" type="submit">{e(t["subscribe"])}</button></form>')
    return f'<p class="soon">{e(t["subscribe_soon"])}</p>'


def featured_project(vis, briefs):
    by_id = {p["id"]: p for p in vis}
    if briefs and (briefs[0].get("deal") or {}).get("project_id") in by_id:
        return by_id[briefs[0]["deal"]["project_id"]], briefs[0]["deal"]
    score = lambda p: (p["milestones"][0]["date"][:7], p.get("cost") is not None, p["stage"], len(p["milestones"]))
    return max(vis, key=score), None


def africa_map(lang, vis):
    t = T[lang]
    counts = {}
    for p in vis:
        for c in codes_of(p):
            counts[c] = counts.get(c, 0) + 1
    shapes = []
    for code, d in AFRICA["paths"].items():
        n = counts.get(code, 0)
        if n and code in COUNTRIES:
            name = country_name(code, lang)
            lvl = min(n, 3)
            shapes.append(f'<path class="land on l{lvl}" d="{d}" data-country="{code}" tabindex="0" role="button" '
                          f'aria-label="{e(name)} : {e(plural(lang, n))}"><title>{e(name)} : {e(plural(lang, n))}</title></path>')
        else:
            shapes.append(f'<path class="land" d="{d}"/>')
    # Petits États insulaires : un repère circulaire pour rester visibles.
    for code in ("CV", "KM", "MU", "SC", "ST"):
        if counts.get(code) and code in AFRICA["centroids"]:
            x, y = AFRICA["centroids"][code]
            shapes.append(f'<circle class="land on l1" cx="{x}" cy="{y}" r="6" data-country="{code}"/>')
    return (f'<svg class="map" viewBox="{AFRICA["viewBox"]}" role="group" aria-label="{e(t["map_label"])}">'
            f'{"".join(shapes)}</svg>')


def build_home(lang, projects, briefs, updated):
    t = T[lang]
    vis = sorted(visible(projects), key=lambda p: p["milestones"][0]["date"], reverse=True)
    feat, deal = featured_project(vis, briefs)
    countries = sorted({c for p in vis for c in codes_of(p)}, key=lambda c: country_name(c, lang))
    counts = [sum(1 for p in vis if p["stage"] == i) for i in range(5)]

    # À la une
    f_link = url(lang, t["projects_slug"], feat["id"])
    f_title = deal["title"][lang] if deal else feat["name"][lang]
    f_text = feat["summary"][lang]
    f_facts = [(t["f_stage"], e(t["stages"][feat["stage"]]))]
    if feat.get("capacity"):
        f_facts.append((t["f_capacity"], e(lx(feat["capacity"], lang))))
    if feat.get("cost"):
        note = cost_note(feat["cost"], lang)
        f_facts.append((t["f_cost"], e(fmt_amount(feat["cost"], lang)) + (f"<small>{e(note)}</small>" if note else "")))
    facts_html = "".join(f'<div><dt>{e(k)}</dt><dd>{v}</dd></div>' for k, v in f_facts)

    # Ce qui a bougé : derniers jalons, tous projets confondus
    events = sorted(((m["date"], p, m) for p in vis for m in p["milestones"] if p["id"] != feat["id"]),
                    key=lambda x: x[0], reverse=True)[:5]
    moved = "".join(
        f'<li><a href="{url(lang, t["projects_slug"], p["id"])}"><span class="mv-meta"><span class="sector s-{e(p["sector"])}">{icon(p["sector"])}</span>'
        f'{e(country_name(p["country"], lang))}<time datetime="{e(d)}">{e(fmt_date(d, lang))}</time></span>'
        f'<strong>{e(p["name"][lang])}</strong><span class="mv-text">{e(m["text"][lang])}</span></a></li>'
        for d, p, m in events)

    # Répartition par secteur
    sec_counts = [(k, sum(1 for p in vis if p["sector"] == k)) for k in t["sectors"]]
    smax = max(n for _, n in sec_counts) or 1
    sectors_html = "".join(
        f'<li><span class="bs-l">{icon(k)}{e(t["sectors"][k])}</span><span class="bs-bar"><span style="width:{round(n / smax * 100)}%"></span></span><span class="bs-n">{n}</span></li>'
        for k, n in sec_counts if n)

    # Montants annoncés
    with_cost = [p for p in vis if p.get("cost")]
    def amount_item(p):
        note = cost_note(p["cost"], lang)
        note_html = f'<span class="am-n">{e(note)}</span>' if note else ""
        return (f'<li><a href="{url(lang, t["projects_slug"], p["id"])}"><span class="am-v">{e(fmt_amount(p["cost"], lang))}</span>'
                f'<span class="am-p">{e(p["name"][lang])}, {e(country_name(p["country"], lang))}</span>{note_html}</a></li>')
    amounts = "".join(amount_item(p) for p in sorted(with_cost, key=lambda p: p["cost"]["amount"], reverse=True))
    amounts_html = (f'<div class="amounts"><h3>{e(t["amounts"])}</h3><ul>{amounts}</ul>'
                    f'<p class="fine">{e(t["amounts_note"])}</p></div>') if amounts else ""

    # Filtres
    pills = [f'<button type="button" class="pill" aria-pressed="true" data-sector="">{e(t["all"])} <span>{len(vis)}</span></button>']
    for key, label in t["sectors"].items():
        n = sum(1 for p in vis if p["sector"] == key)
        if n:
            pills.append(f'<button type="button" class="pill" aria-pressed="false" data-sector="{key}">{icon(key)}{e(label)} <span>{n}</span></button>')
    options = "".join(f'<option value="{c}">{e(country_name(c, lang))}</option>' for c in countries)
    banner = f'<p class="notice">{e(t["unverified_banner"])}</p>' if any(p["status"] != "publié" for p in vis) else ""
    cards = "\n".join(card(p, lang) for p in vis)

    body = f"""
<section class="une" aria-labelledby="une-t">
<div class="wrap une-in">
<article class="une-main">
<p class="une-label">{e(t['featured'])}</p>
<p class="une-kick"><span class="sector s-{e(feat['sector'])}">{icon(feat['sector'])}{e(t['sectors'][feat['sector']])}</span><span class="country">{e(country_name(feat['country'], lang))}</span></p>
<h1 id="une-t"><a href="{f_link}">{e(f_title)}</a></h1>
<p class="lede">{e(f_text)}</p>
{route(feat['stage'], lang, size="md")}
<dl class="une-facts">{facts_html}</dl>
<a class="btn" href="{f_link}">{e(t['read_project'])}</a>
</article>
<aside class="une-side" aria-labelledby="mv-t">
<h2 id="mv-t">{e(t['this_week'])}</h2>
<ol class="moved-list">{moved}</ol>
</aside>
</div>
</section>

<section class="band" aria-labelledby="pl">
<div class="wrap band-in">
<div class="band-main">
<h2 id="pl">{e(t['pipeline'])}</h2>
<p class="band-sum">{e(t['pipeline_sum'].format(n=len(vis), c=len(countries), d=fmt_date(updated, lang)))} {e(t['pipeline_note'])}</p>
{route(None, lang, size="lg", counts=counts)}
<h3 class="by-sector-t">{e(t['by_sector'])}</h3>
<ul class="by-sector">{sectors_html}</ul>
</div>
{amounts_html}
</div>
</section>

<section class="wrap explore" aria-labelledby="ex">
<div class="explore-head"><h2 id="ex">{e(t['explore'])}</h2>{banner}</div>
<div class="explore-in">
<aside class="map-box">
<h3>{e(t['map_title'])}</h3>
{africa_map(lang, vis)}
<p class="fine">{e(t['map_hint'])}</p>
</aside>
<div class="explore-main">
<div class="filters">
<div class="pills" role="group" aria-label="{e(t['filter_sector'])}">{''.join(pills)}</div>
<div class="filter-row">
<label class="search"><span class="sr">{e(t['search_label'])}</span><svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="7" cy="7" r="5"/><line x1="11" y1="11" x2="15" y2="15"/></svg><input type="search" id="q" placeholder="{e(t['search'])}"></label>
<label class="select"><span class="sr">{e(t['country_filter'])}</span><select id="country"><option value="">{e(t['all_countries'])}</option>{options}</select></label>
</div>
</div>
<p class="count" id="count" aria-live="polite"></p>
<div class="cards" id="cards">
{cards}
</div>
<div class="empty" id="empty" hidden><p>{e(t['no_result'])}</p><button type="button" class="btn-ghost" id="reset">{e(t['reset'])}</button></div>
</div>
</div>
</section>

<section class="brief-band" aria-labelledby="br">
<div class="wrap brief-in">
<div><h2 id="br">{e(t['brief_title'])}</h2><p>{e(t['brief_pitch'])}</p></div>
<a class="btn btn-light" href="{url(lang, t['brief_slug'])}">{e(t['subscribe'])}</a>
</div>
</section>
<script>
(function(){{
  var one={json.dumps(T[lang]['n_projects'][1])}, many={json.dumps(T[lang]['n_projects']['n'])};
  var pills=[].slice.call(document.querySelectorAll('.pill')),cards=[].slice.call(document.querySelectorAll('#cards .card'));
  var lands=[].slice.call(document.querySelectorAll('.map .on'));
  var q=document.getElementById('q'),sel=document.getElementById('country'),empty=document.getElementById('empty'),count=document.getElementById('count'),sector='';
  function apply(){{
    var term=(q.value||'').toLowerCase().trim(),c=sel.value,n=0;
    cards.forEach(function(el){{
      var ok=(!sector||el.dataset.sector===sector)&&(!c||el.dataset.country.split(',').indexOf(c)>-1)&&(!term||el.dataset.text.indexOf(term)>-1);
      el.hidden=!ok; if(ok)n++;
    }});
    lands.forEach(function(l){{l.classList.toggle('sel',!!c&&l.dataset.country===c);}});
    empty.hidden=n>0; count.textContent=n===1?one:many.replace('{{n}}',n);
  }}
  function pick(code){{sel.value=(sel.value===code?'':code);apply();}}
  pills.forEach(function(b){{b.addEventListener('click',function(){{sector=b.dataset.sector;pills.forEach(function(x){{x.setAttribute('aria-pressed',x===b?'true':'false');}});apply();}});}});
  lands.forEach(function(l){{l.addEventListener('click',function(){{pick(l.dataset.country);}});l.addEventListener('keydown',function(ev){{if(ev.key==='Enter'||ev.key===' '){{ev.preventDefault();pick(l.dataset.country);}}}});}});
  document.getElementById('reset').addEventListener('click',function(){{q.value='';sel.value='';sector='';pills.forEach(function(x,i){{x.setAttribute('aria-pressed',i===0?'true':'false');}});apply();}});
  q.addEventListener('input',apply);sel.addEventListener('change',apply);apply();
}})();
</script>
"""
    return page(lang, NAME, body, [], current="nav_projects")


def build_project(lang, p, projects):
    t = T[lang]
    joined = lambda xs: ", ".join(lx(x, lang) for x in xs) if xs else None
    rows = [
        (t["f_cost"], fmt_amount(p.get("cost"), lang)),
        (t["f_capacity"], lx(p.get("capacity"), lang)),
        (t["f_owner"], joined(p.get("owner"))),
        (t["f_lenders"], joined(p.get("lenders"))),
        (t["f_contractors"], joined(p.get("contractors"))),
        (t["f_target"], p.get("target_date")),
    ]
    known = [(k, v) for k, v in rows if v]
    unknown = [k for k, v in rows if not v]
    base = [(t["f_country"], country_name(p["country"], lang)), (t["f_sector"], t["sectors"][p["sector"]]),
            (t["f_stage"], t["stages"][p["stage"]])]
    note = cost_note(p.get("cost"), lang)
    cell = lambda k, v: e(v) + (f'<small>{e(note)}</small>' if k == t["f_cost"] and note else "")
    table = "".join(f'<tr><th scope="row">{e(k)}</th><td>{cell(k, v)}</td></tr>' for k, v in base + known)
    missing = ""
    if unknown:
        low = lambda k: k if k[:2].isupper() else k[0].lower() + k[1:]
        lst = ", ".join(low(k) for k in unknown)
        missing = f'<p class="missing">{e(t["missing"].format(x=lst))}</p>'
    ms_html = []
    for m in p["milestones"]:
        srcs = ", ".join(
            f'<a href="{e(s["url"])}" rel="noopener" target="_blank">{e(lx(s["publisher"], lang))}</a>' for s in m["sources"])
        ok = m["confidence"] == "confirmé"
        conf = t["confirmed"] if ok else t["unverified"]
        ms_html.append(
            f'<li class="{"ok" if ok else "tbc"}"><div class="tl-meta"><time datetime="{e(m["date"])}">{e(fmt_date(m["date"], lang))}</time>'
            f'<span class="conf">{e(conf)}</span></div>'
            f'<p>{e(m["text"][lang])}</p><p class="src">{e(t["sources"])}{" :" if lang == "fr" else ":"} {srcs}</p></li>')
    related = [r for r in visible(projects) if r["sector"] == p["sector"] and r["id"] != p["id"]][:4]
    rel_html = "".join(
        f'<li><a href="{url(lang, t["projects_slug"], r["id"])}"><strong>{e(r["name"][lang])}</strong>'
        f'<span>{e(country_name(r["country"], lang))}, {e(t["stages"][r["stage"]].lower())}</span></a></li>' for r in related)
    corr = p.get("corrections") or []
    corr_html = ""
    if corr:
        items = "".join(f'<li><time datetime="{e(c["date"])}">{e(fmt_date(c["date"], lang))}</time> {e(c["text"][lang])}</li>'
                        for c in corr)
        corr_html = f'<section class="panel corrections" id="corrections"><h2>{e(t["corrections"])}</h2><ul>{items}</ul></section>'
    badge = f'<span class="badge">{e(t["unverified"])}</span>' if p["status"] != "publié" else ""
    body = f"""
<div class="wrap project">
<a class="back" href="{url(lang)}">{e(t['back'])}</a>
<header class="project-head">
<div class="project-meta"><span class="sector s-{e(p['sector'])}">{icon(p['sector'])}{e(t['sectors'][p['sector']])}</span><span class="strong">{e(country_name(p['country'], lang))}</span><span>{e(t['updated'])} {e(fmt_date(p['updated'], lang))}</span>{badge}</div>
<h1>{e(p['name'][lang])}</h1>
<p class="lede">{e(p['summary'][lang])}</p>
</header>
<section class="stage-box" aria-label="{e(t['stage'])}">{route(p['stage'], lang, size="md")}</section>
<div class="layout">
<div class="col-main">
<section class="panel"><h2>{e(t['facts'])}</h2><div class="table-scroll"><table class="facts">{table}</table></div>{missing}</section>
<section class="panel"><h2>{e(t['milestones'])}</h2><ol class="timeline">{''.join(ms_html)}</ol></section>
{corr_html}
</div>
<aside class="col-side">
<section class="panel panel-ink"><h2>{e(t['brief_title'])}</h2><p>{e(t['brief_side'])}</p><a class="btn btn-light btn-block" href="{url(lang, t['brief_slug'])}">{e(t['subscribe'])}</a></section>
{f'<section class="panel"><h2>{e(t["same_sector"])}</h2><ul class="related">{rel_html}</ul></section>' if rel_html else ''}
</aside>
</div>
</div>"""
    return page(lang, p["name"][lang], body, [t["projects_slug"], p["id"]], p["summary"][lang], current="nav_projects", kind="article")


def paragraphs(text):
    return "".join(f"<p>{e(par.strip())}</p>" for par in str(text).split("\n\n") if par.strip())


def build_brief_issue(lang, b, by_id):
    t = T[lang]
    moved = "".join(
        f'<li><a href="{url(lang, t["projects_slug"], m["project_id"])}"><strong>{e(country_name(by_id[m["project_id"]]["country"], lang))}</strong></a> : {e(m["line"][lang])}</li>'
        for m in b.get("moved") or [])
    deal = ""
    if b.get("deal"):
        deal = f'<h2>{e(t["deal"])}</h2><h3>{e(b["deal"]["title"][lang])}</h3>{paragraphs(b["deal"]["body"][lang])}'
    analysis = ""
    if b.get("analysis"):
        analysis = (f'<h2>{e(t["analysis"])}</h2><p class="tag">{e(t["analysis_tag"])}</p>'
                    f'<h3>{e(b["analysis"]["title"][lang])}</h3>{paragraphs(b["analysis"]["body"][lang])}')
    title = f'{t["brief_title"]}, {t["issue"].format(n=b["number"], d=fmt_date(b["date"], lang))}'
    body = f"""
<div class="wrap narrow prose issue">
<a class="back" href="{url(lang, t['brief_slug'])}">{e(t['brief_title'])}</a>
<p class="issue-no">{e(t['issue'].format(n=b['number'], d=fmt_date(b['date'], lang)))}</p>
<h1>{e(t['brief_title'])}</h1>
<h2>{e(t['moved'])}</h2><ol class="moved">{moved}</ol>
{deal}
{analysis}
</div>"""
    lead = b["deal"]["title"][lang] if b.get("deal") else ""
    return page(lang, title, body, [t["brief_slug"], b["date"]], lead, current="nav_brief", kind="article")


def build_brief_index(lang, briefs):
    t = T[lang]
    items = "".join(
        f'<li><a href="{url(lang, t["brief_slug"], b["date"])}">{e(t["issue"].format(n=b["number"], d=fmt_date(b["date"], lang)))}</a></li>'
        for b in briefs)
    archive = f'<ul class="archive">{items}</ul>' if items else f'<p class="muted">{e(t["no_brief"])}</p>'
    body = f"""
<div class="wrap narrow prose">
<h1>{e(t['brief_title'])}</h1>
<p class="lead">{e(t['brief_pitch'])}</p>
<div class="panel signup-box">{newsletter_box(lang)}</div>
<h2>{e(t['archive'])}</h2>
{archive}
</div>"""
    return page(lang, t["brief_title"], body, [t["brief_slug"]], current="nav_brief")


def build_method(lang):
    t = T[lang]
    body = f'<div class="wrap narrow prose"><h1>{e(t["method_title"])}</h1>{METHOD[lang]}</div>'
    return page(lang, t["method_title"], body, [t["method_slug"]], current="nav_method")


def build_about(lang):
    t = T[lang]
    body = (f'<div class="wrap narrow prose"><h1>{e(t["about_title"])}</h1>'
            f'<p class="signature">{e(t["about_sub"])}</p>{ABOUT[lang]}</div>')
    return page(lang, t["about_title"], body, [t["about_slug"]], current="nav_about")


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
    for lang in LANGS:
        if (SITE / f"og-{lang}.png").exists():
            shutil.copy(SITE / f"og-{lang}.png", DIST / "assets" / f"og-{lang}.png")
    if TRACKING:
        shutil.copy(SITE / "audience.js", DIST / "assets" / "audience.js")
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
        write(f"{lang}/{t['about_slug']}", build_about(lang))
        pages += 3
        for p in visible(projects):
            write(f"{lang}/{t['projects_slug']}/{p['id']}", build_project(lang, p, projects))
            pages += 1
        for b in briefs:
            write(f"{lang}/{t['brief_slug']}/{b['date']}", build_brief_issue(lang, b, by_id))
            pages += 1
    if ORIGIN:
        # Plan du site et robots.txt, pour que Google trouve chaque fiche projet.
        # Sur GitHub Pages en sous-dossier, Google lit le sitemap déclaré dans la Search Console.
        stamp = date.today().isoformat()
        urls = "".join(f"<url><loc>{e(u)}</loc><lastmod>{stamp}</lastmod></url>" for u in sorted(set(SITEMAP)))
        (DIST / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
        (DIST / "robots.txt").write_text(
            f"User-agent: *\nAllow: /\nSitemap: {ORIGIN}{BASE}/sitemap.xml\n", encoding="utf-8")
    print(f"Site généré : {pages} pages dans dist/")


if __name__ == "__main__":
    main()
