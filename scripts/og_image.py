"""Génère les images de partage du site (site/og-fr.png et site/og-en.png, 1200 x 630).

Ce sont les images qui s'affichent quand un lien Koridor est partagé sur LinkedIn,
WhatsApp, X ou par e-mail. Elles sont commises dans le dépôt : le site reste généré sans
dépendance. À relancer seulement si l'identité visuelle change.

Usage :
  pip install pillow
  npm pack @fontsource/archivo @fontsource/source-serif-4   (dans un dossier de travail)
  python3 scripts/og_image.py --fonts /chemin/vers/le/dossier/des/paquets
"""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
INK, GREEN, GREEN_L, YELLOW, BG = "#0F1E2B", "#127A5A", "#2BB383", "#F2B705", "#F3F5F4"
W, H = 1200, 630

TEXT = {
    "fr": ("Comprendre les infrastructures", "qui transforment l'Afrique.",
           "Projets suivis de l'annonce à la mise en service · Brief chaque lundi",
           ("Identification", "Passation", "Financement", "Construction", "Exploitation")),
    "en": ("Understanding the infrastructure", "transforming Africa.",
           "Projects tracked from announcement to commissioning · Brief every Monday",
           ("Identification", "Procurement", "Financing", "Construction", "Operation")),
}


def font(fonts, name, size):
    hits = sorted(Path(fonts).rglob(name))
    if not hits:
        raise SystemExit(f"Police introuvable : {name} dans {fonts}")
    return ImageFont.truetype(str(hits[0]), size)


def draw(lang, fonts):
    l1, l2, sub, stages = TEXT[lang]
    im = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(im)
    # Logo : le K formé de deux voies
    x0, y0, s = 80, 72, 2.4
    d.line([(x0 + 8 * s, y0 + 3 * s), (x0 + 8 * s, y0 + 27 * s)], fill="white", width=9)
    d.line([(x0 + 8 * s, y0 + 15 * s), (x0 + 25 * s, y0 + 4 * s)], fill=YELLOW, width=9)
    d.line([(x0 + 8 * s, y0 + 15 * s), (x0 + 25 * s, y0 + 26 * s)], fill=GREEN_L, width=9)
    d.text((x0 + 80, y0 + 2), "Koridor", font=font(fonts, "archivo-latin-800-normal.woff", 62), fill="white")
    title = font(fonts, "archivo-latin-700-normal.woff", 64)
    d.text((80, 220), l1, font=title, fill="white")
    d.text((80, 298), l2, font=title, fill=GREEN_L)
    d.text((80, 392), sub, font=font(fonts, "source-serif-4-latin-400-normal.woff", 27), fill="#C9D3DA")
    # La ligne de corridor : cinq stades, le troisième en cours
    y, xs = 520, [80 + i * 250 for i in range(5)]
    d.line([(xs[0], y), (xs[2], y)], fill=GREEN_L, width=6)
    d.line([(xs[2], y), (xs[4], y)], fill="#3A4B58", width=6)
    small = font(fonts, "archivo-latin-400-normal.woff", 22)
    for i, x in enumerate(xs):
        r = 13
        if i < 2:
            d.ellipse([x - r, y - r, x + r, y + r], fill=GREEN_L)
        elif i == 2:
            d.ellipse([x - r - 4, y - r - 4, x + r + 4, y + r + 4], fill=YELLOW, outline="white", width=4)
        else:
            d.ellipse([x - r, y - r, x + r, y + r], fill=INK, outline="#5B6C78", width=4)
        anchor = "la" if i == 0 else "ra" if i == 4 else "ma"
        tx = x - r if i == 0 else x + r if i == 4 else x
        d.text((tx, y + 30), stages[i], font=small, fill="#C9D3DA", anchor=anchor)
    out = ROOT / "site" / f"og-{lang}.png"
    im.save(out, optimize=True)
    print(f"Écrit : {out.relative_to(ROOT)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--fonts", required=True, help="dossier contenant les paquets @fontsource décompressés")
    args = ap.parse_args()
    for lang in TEXT:
        draw(lang, args.fonts)
