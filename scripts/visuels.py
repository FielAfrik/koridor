"""Visuels de la semaine pour les réseaux, générés à partir du Brief (agent C3, Studio visuel).

Produit, dans le dossier de sortie :
  carrousel-<lang>.pdf          le carrousel « Ce qui a bougé » (1080 x 1350, une page par projet)
  carrousel-<lang>-NN.png       les mêmes pages en images (aperçu, WhatsApp)
  deal-<lang>.png               le deal de la semaine (1200 x 1200)
  echeances-<lang>.png          les dates limites citées dans le Brief (1200 de large)

Aucun chiffre n'est tapé à la main : tout vient du Brief et de data/projects.json.

Usage :
  pip install pillow
  python3 scripts/visuels.py --brief 2026-10-19 --fonts DOSSIER_POLICES --out DOSSIER [--lang fr]
(DOSSIER_POLICES : paquets @fontsource/archivo et @fontsource/source-serif-4 décompressés,
 voir scripts/og_image.py.)
"""
import argparse
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
INK, GREEN, GREEN_L, YELLOW, BG, MUTED, LINE = (
    "#0F1E2B", "#127A5A", "#2BB383", "#F2B705", "#F3F5F4", "#5B6C78", "#D5DCE0")
SITE = "fielafrik.github.io/koridor"

L = {
    "fr": {
        "stages": ("Identification", "Passation", "Financement", "Construction", "Exploitation"),
        "sectors": {"energie": "Énergie", "transport": "Transport", "eau": "Eau", "numerique": "Villes & numérique"},
        "cover_kicker": "Le Brief du lundi · n° {n}",
        "cover_title": "Ce qui a bougé cette semaine",
        "cover_sub": "{k} projets d'infrastructure et d'énergie en Afrique, vérifiés à la source.",
        "swipe": "Faites défiler",
        "week": "Cette semaine",
        "stage_now": "Stade actuel : {s}",
        "amount": "Montant annoncé",
        "total": "Coût total annoncé : {a}",
        "capacity": "Capacité", "lenders": "Financeurs", "owner": "Maître d'ouvrage",
        "end_title": "Toutes les fiches, sources comprises",
        "end_body": "Chaque projet a sa fiche : stade, financeurs, chronologie et liens vers les sources officielles.",
        "end_follow": "Prochain Brief lundi prochain.",
        "deal_kicker": "Le deal de la semaine",
        "deadlines_kicker": "Échéances",
        "deadlines_title": "Les dates limites à noter",
        "deadlines_note": "Dates telles qu'annoncées par les maîtres d'ouvrage.",
        "by": "par {a}",
        "months": ("janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
                   "septembre", "octobre", "novembre", "décembre"),
    },
    "en": {
        "stages": ("Identification", "Procurement", "Financing", "Construction", "Operation"),
        "sectors": {"energie": "Energy", "transport": "Transport", "eau": "Water", "numerique": "Cities & digital"},
        "cover_kicker": "The Monday Brief · No. {n}",
        "cover_title": "What moved this week",
        "cover_sub": "{k} infrastructure and energy projects in Africa, checked at the source.",
        "swipe": "Swipe",
        "week": "This week",
        "stage_now": "Current stage: {s}",
        "amount": "Announced amount",
        "total": "Total announced cost: {a}",
        "capacity": "Capacity", "lenders": "Lenders", "owner": "Project owner",
        "end_title": "Every project file, sources included",
        "end_body": "Each project has its own page: stage, lenders, timeline and links to official sources.",
        "end_follow": "Next Brief next Monday.",
        "deal_kicker": "Deal of the week",
        "deadlines_kicker": "Deadlines",
        "deadlines_title": "Dates to note",
        "deadlines_note": "Dates as announced by project owners.",
        "by": "by {a}",
        "months": ("January", "February", "March", "April", "May", "June", "July", "August",
                   "September", "October", "November", "December"),
    },
}


class Fonts:
    def __init__(self, folder):
        self.folder = Path(folder)

    def get(self, family, weight, size):
        name = f"{family}-latin-{weight}-normal.woff"
        hits = sorted(self.folder.rglob(name))
        if not hits:
            raise SystemExit(f"Police introuvable : {name} dans {self.folder}")
        return ImageFont.truetype(str(hits[0]), size)

    def sans(self, size, weight=700):
        return self.get("archivo", weight, size)

    def serif(self, size, weight=400):
        return self.get("source-serif-4", weight, size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def block(d, xy, text, font, width, fill, spacing=1.3):
    x, y = xy
    size = font.size
    for line in wrap(d, text, font, width):
        d.text((x, y), line, font=font, fill=fill)
        y += int(size * spacing)
    return y


def logo(d, x, y, s, fonts, color="white", word=True):
    w = max(3, int(3.6 * s))
    d.line([(x + 8 * s, y + 3 * s), (x + 8 * s, y + 27 * s)], fill=color, width=w)
    d.line([(x + 8 * s, y + 15 * s), (x + 25 * s, y + 4 * s)], fill=YELLOW, width=w)
    d.line([(x + 8 * s, y + 15 * s), (x + 25 * s, y + 26 * s)], fill=GREEN_L if color == "white" else GREEN, width=w)
    if word:
        d.text((x + 33 * s, y + 2 * s), "Koridor", font=fonts.sans(int(22 * s), 800), fill=color)


def corridor(d, x0, x1, y, stage, labels, fonts, dark=False):
    xs = [x0 + i * (x1 - x0) / 4 for i in range(5)]
    done, todo = (GREEN_L if dark else GREEN), ("#3A4B58" if dark else LINE)
    d.line([(xs[0], y), (xs[stage], y)], fill=done, width=8)
    d.line([(xs[stage], y), (xs[4], y)], fill=todo, width=8)
    f = fonts.sans(24, 400)
    for i, x in enumerate(xs):
        r = 15
        if i < stage:
            d.ellipse([x - r, y - r, x + r, y + r], fill=done)
        elif i == stage:
            d.ellipse([x - r - 5, y - r - 5, x + r + 5, y + r + 5], fill=YELLOW, outline=("white" if dark else INK), width=5)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=(INK if dark else "white"), outline=todo, width=5)
        anchor, tx = ("la", x - r) if i == 0 else ("ra", x + r) if i == 4 else ("ma", x)
        col = ("white" if dark else INK) if i == stage else ("#C9D3DA" if dark else MUTED)
        d.text((tx, y + 34), labels[i], font=fonts.sans(24, 700) if i == stage else f, fill=col, anchor=anchor)


def amount_text(cost, lang):
    if not cost:
        return None
    a = cost["amount"]
    cur = cost["currency"]
    unit = cost.get("unit", "")
    if lang == "fr":
        num = (f"{a:,.2f}".rstrip("0").rstrip(".") if isinstance(a, float) else f"{a:,}").replace(",", " ").replace(".", ",")
        word = {"millions": "millions", "milliards": "milliards"}.get(unit, unit)
        dev = {"EUR": "d'euros", "USD": "de dollars", "XOF": "de francs CFA", "XAF": "de francs CFA"}.get(cur, cur)
        return f"{num} {word} {dev}".replace("  ", " ")
    num = f"{a:,.2f}".rstrip("0").rstrip(".") if isinstance(a, float) else f"{a:,}"
    sym = {"EUR": "€", "USD": "$"}.get(cur)
    word = {"millions": "million", "milliards": "billion"}.get(unit, unit)
    return f"{sym}{num} {word}" if sym else f"{num} {word} {cur}"


def arrow(d, x, y, color):
    d.line([(x, y), (x + 30, y)], fill=color, width=5)
    d.polygon([(x + 34, y), (x + 20, y - 11), (x + 20, y + 11)], fill=color)


def value(v, lang):
    if not v:
        return None
    if isinstance(v, dict):
        return v.get(lang)
    if isinstance(v, list):
        names = [value(x, lang) for x in v]
        return ", ".join(n for n in names if n) or None
    return str(v)


def fact_panel(d, p, lang, fonts, bottom=1205):
    """Encadré de la fiche, ancré en bas de page : montant, capacité, financeurs, maître d'ouvrage."""
    t = L[lang]
    small, label_f, val_f = fonts.serif(27), fonts.sans(25, 400), fonts.sans(32, 700)
    rows = []
    amt = amount_text(p.get("cost"), lang)
    if amt:
        note = (p["cost"].get("note") or {}).get(lang)
        rows.append(("amount", t["amount"], amt, wrap(d, note, small, 840)[:2] if note else []))
    for key in ("capacity", "lenders", "owner"):
        v = value(p.get(key), lang)
        if v:
            rows.append((key, t[key], wrap(d, v, val_f, 840)[:2], []))
    if not rows:
        return
    heights = []
    for kind, _, v, note in rows:
        heights.append(34 + (66 if kind == "amount" else 42 * len(v)) + 36 * len(note) + 22)
    top = bottom - sum(heights) - 30
    d.rounded_rectangle([80, top, 1000, bottom], radius=18, fill="white", outline=LINE, width=2)
    y = top + 26
    for (kind, label, v, note), h in zip(rows, heights):
        d.text((112, y), label, font=label_f, fill=MUTED)
        if kind == "amount":
            d.text((112, y + 32), v, font=fonts.sans(50, 800), fill=INK)
            yy = y + 100
        else:
            yy = y + 34
            for line in v:
                d.text((112, yy), line, font=val_f, fill=INK)
                yy += 42
        for line in note:
            d.text((112, yy), line, font=small, fill=MUTED)
            yy += 36
        y += h
        if h is not heights[-1]:
            d.line([(112, y - 12), (968, y - 12)], fill=LINE, width=1)


def footer(d, fonts, page, total, author, lang, dark=False):
    col = "#C9D3DA" if dark else MUTED
    d.line([(80, 1250), (1000, 1250)], fill=("#2A3B48" if dark else LINE), width=2)
    logo(d, 80, 1270, 1.5, fonts, color=("white" if dark else INK))
    right = f"{L[lang]['by'].format(a=author)} · {page}/{total}" if author else f"{page}/{total}"
    d.text((1000, 1282), right, font=fonts.sans(24, 400), fill=col, anchor="ra")


def carousel(brief, projects, countries, lang, fonts, out, author):
    t = L[lang]
    moved = [m for m in brief.get("moved") or [] if m["project_id"] in projects]
    total = len(moved) + 2
    pages = []

    # Couverture
    im = Image.new("RGB", (1080, 1350), INK)
    d = ImageDraw.Draw(im)
    logo(d, 80, 90, 2.2, fonts)
    d.text((80, 300), t["cover_kicker"].format(n=brief["number"]), font=fonts.sans(34, 700), fill=YELLOW)
    y = block(d, (80, 360), t["cover_title"], fonts.sans(96, 800), 900, "white", 1.08)
    y = block(d, (80, y + 30), t["cover_sub"].format(k=len(moved)), fonts.serif(38), 880, "#C9D3DA", 1.35)
    # Liste des pays, comme une ligne de stations
    yy = max(y + 70, 860)
    for m in moved[:6]:
        p = projects[m["project_id"]]
        c = " / ".join(countries.get(code, [code, code])[0 if lang == "fr" else 1] for code in p["country"].split(","))
        d.ellipse([86, yy + 8, 106, yy + 28], fill=GREEN_L)
        d.text((126, yy), f"{c} — {t['sectors'].get(p['sector'], p['sector'])}", font=fonts.sans(30, 400), fill="white")
        yy += 52
    d.text((950, 1180), t["swipe"], font=fonts.sans(30, 700), fill=YELLOW, anchor="ra")
    arrow(d, 966, 1198, YELLOW)
    footer(d, fonts, 1, total, author, lang, dark=True)
    pages.append(im)

    # Une page par projet
    for i, m in enumerate(moved, start=2):
        p = projects[m["project_id"]]
        im = Image.new("RGB", (1080, 1350), BG)
        d = ImageDraw.Draw(im)
        country = " / ".join(countries.get(c, [c, c])[0 if lang == "fr" else 1] for c in p["country"].split(","))
        sector = t["sectors"].get(p["sector"], p["sector"])
        d.rectangle([0, 0, 1080, 14], fill=GREEN)
        d.text((80, 80), country, font=fonts.sans(40, 800), fill=GREEN)
        d.text((1000, 88), sector, font=fonts.sans(30, 400), fill=MUTED, anchor="ra")
        y = block(d, (80, 150), p["name"][lang], fonts.sans(58, 800), 920, INK, 1.12)
        corridor(d, 110, 970, y + 70, p["stage"], t["stages"], fonts)
        y += 190
        d.text((80, y), t["week"], font=fonts.sans(28, 700), fill=MUTED)
        y = block(d, (80, y + 46), m["line"][lang], fonts.serif(44), 920, INK, 1.32)
        fact_panel(d, p, lang, fonts)
        footer(d, fonts, i, total, author, lang)
        pages.append(im)

    # Dernière page
    im = Image.new("RGB", (1080, 1350), INK)
    d = ImageDraw.Draw(im)
    logo(d, 80, 90, 2.2, fonts)
    y = block(d, (80, 330), t["end_title"], fonts.sans(80, 800), 920, "white", 1.1)
    y = block(d, (80, y + 30), t["end_body"], fonts.serif(38), 880, "#C9D3DA", 1.35)
    d.rounded_rectangle([80, y + 60, 1000, y + 170], radius=18, fill=GREEN)
    d.text((540, y + 115), SITE, font=fonts.sans(44, 700), fill="white", anchor="mm")
    d.text((80, y + 230), t["end_follow"], font=fonts.sans(34, 700), fill=YELLOW)
    footer(d, fonts, total, total, author, lang, dark=True)
    pages.append(im)

    for n, im in enumerate(pages, start=1):
        im.save(out / f"carrousel-{lang}-{n:02d}.png", optimize=True)
    pdf = out / f"carrousel-{lang}.pdf"
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=150)
    return pdf


AMOUNT_RE = {
    "fr": re.compile(r"\d[\d  ]*(?:,\d+)?\s(?:millions?|milliards?)\s(?:d'euros|de dollars|de francs CFA)"),
    "en": re.compile(r"[€$]\d[\d,]*(?:\.\d+)?\s(?:million|billion)"),
}


def deal(brief, projects, countries, lang, fonts, out, author):
    t = L[lang]
    dl = brief.get("deal")
    if not dl or dl["project_id"] not in projects:
        return None
    p = projects[dl["project_id"]]
    title = dl["title"][lang]
    m = AMOUNT_RE[lang].search(title) or AMOUNT_RE[lang].search(dl["body"][lang])
    im = Image.new("RGB", (1200, 1200), INK)
    d = ImageDraw.Draw(im)
    logo(d, 80, 80, 2.0, fonts)
    d.text((80, 230), t["deal_kicker"], font=fonts.sans(36, 700), fill=YELLOW)
    y = 300
    if m:
        y = block(d, (80, y), m.group(0), fonts.sans(110, 800), 1040, "white", 1.05) + 20
    lender = ", ".join(x[lang] for x in p.get("lenders") or [])
    if lender:
        d.text((80, y), lender, font=fonts.sans(40, 700), fill=GREEN_L)
        y += 70
    country = " / ".join(countries.get(c, [c, c])[0 if lang == "fr" else 1] for c in p["country"].split(","))
    y = block(d, (80, y + 10), f"{country} · {p['name'][lang]}", fonts.serif(44), 1040, "white", 1.3)
    total = amount_text(p.get("cost"), lang)
    if total and m and total != m.group(0):
        block(d, (80, y + 30), t["total"].format(a=total), fonts.serif(36), 1040, "#C9D3DA", 1.35)
    corridor(d, 110, 1090, 1010, p["stage"], t["stages"], fonts, dark=True)
    if author:
        d.text((1120, 105), t["by"].format(a=author), font=fonts.sans(26, 400), fill="#C9D3DA", anchor="ra")
    path = out / f"deal-{lang}.png"
    im.save(path, optimize=True)
    return path


DATE_RE = {
    "fr": re.compile(r"(\d{1,2})(?:er)? (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre) (\d{4})"),
    "en": re.compile(r"(\d{1,2}) (January|February|March|April|May|June|July|August|September|October|November|December) (\d{4})"),
}


def deadlines(brief, projects, countries, lang, fonts, out, author):
    t = L[lang]
    rows = []
    for m in brief.get("moved") or []:
        if m["project_id"] not in projects:
            continue
        found = DATE_RE[lang].search(m["line"][lang])
        if not found:
            continue
        day, month, year = found.groups()
        key = (int(year), t["months"].index(month), int(day))
        rows.append((key, f"{day} {month} {year}", projects[m["project_id"]], m["line"][lang]))
    if not rows:
        return None
    rows.sort(key=lambda r: r[0])
    rows = rows[:5]
    H = max(1200, 360 + 330 * len(rows) + 120)
    im = Image.new("RGB", (1200, H), BG)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1200, 300], fill=INK)
    logo(d, 80, 70, 2.0, fonts)
    d.text((80, 190), t["deadlines_kicker"], font=fonts.sans(34, 700), fill=YELLOW)
    d.text((80, 232), t["deadlines_title"], font=fonts.sans(44, 800), fill="white")
    y = 360
    for _, label, p, line in rows:
        country = " / ".join(countries.get(c, [c, c])[0 if lang == "fr" else 1] for c in p["country"].split(","))
        d.rounded_rectangle([80, y, 1120, y + 300], radius=20, fill="white", outline=LINE, width=2)
        d.rectangle([80, y, 92, y + 300], fill=YELLOW)
        d.text((124, y + 30), label, font=fonts.sans(46, 800), fill=INK)
        d.text((124, y + 96), f"{country} · {p['name'][lang]}", font=fonts.sans(30, 700), fill=GREEN)
        block(d, (124, y + 146), line, fonts.serif(32), 960, INK, 1.32)
        y += 330
    d.text((80, H - 90), t["deadlines_note"], font=fonts.serif(28), fill=MUTED)
    d.text((1120, H - 90), SITE, font=fonts.sans(28, 700), fill=GREEN, anchor="ra")
    path = out / f"echeances-{lang}.png"
    im.save(path, optimize=True)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", required=True, help="date du Brief, AAAA-MM-JJ")
    ap.add_argument("--fonts", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--lang", choices=("fr", "en", "all"), default="all")
    ap.add_argument("--author", default="Fiéltoa LARE", help="signature affichée en pied de page (vide pour aucune)")
    a = ap.parse_args()
    brief = json.loads((ROOT / "data" / "briefs" / f"{a.brief}.json").read_text(encoding="utf-8"))
    projects = {p["id"]: p for p in json.loads((ROOT / "data" / "projects.json").read_text(encoding="utf-8"))
                if p["status"] == "publié"}
    countries = json.loads((ROOT / "site" / "countries.json").read_text(encoding="utf-8"))
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    fonts = Fonts(a.fonts)
    for lang in (("fr", "en") if a.lang == "all" else (a.lang,)):
        for fn in (carousel, deal, deadlines):
            path = fn(brief, projects, countries, lang, fonts, out, a.author)
            if path:
                print(f"Écrit : {path}")


if __name__ == "__main__":
    main()
