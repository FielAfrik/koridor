# C3 — Studio visuel

## Mission

Produire les visuels de la semaine aux couleurs de Koridor (`editorial/identite.md`).

## Livrables, dans `work/com/AAAA-MM-JJ/visuels/`

1. **Carrousel « Ce qui a bougé »** (PDF, format 1080 × 1350, 7 pages au plus) :
   - page 1 : titre « Ce qui a bougé — semaine du … », logo, signature ;
   - une page par projet : pays, nom, la ligne de corridor avec le stade actuel en jaune,
     le fait en une phrase, le montant tel qu'annoncé ;
   - dernière page : « Toutes les fiches : Le Brief du lundi » et l'adresse du site.
2. **Visuel du deal** (PNG 1200 × 1200) : le montant en grand, l'institution, le
   projet, le stade.
3. **Visuel des échéances** (PNG 1200 × 1500) : une liste datée.

## Comment

- Lancer `python3 scripts/visuels.py --brief AAAA-MM-JJ --fonts DOSSIER --out
  work/com/AAAA-MM-JJ/visuels` : carrousel PDF (et ses pages en PNG), deal et échéances,
  en français et en anglais. Aucun chiffre n'est retapé à la main.
- Signature en pied de page : « par Fiéltoa LARE » en phase 1 ; `--author ""` en phase 2
  pour les visuels de la page.
- En attendant le script, ou pour un visuel ponctuel, utiliser Canva avec la charte
  Koridor, sans modèle générique.
- Couleurs : encre `#0F1E2B`, vert `#127A5A` / `#2BB383`, jaune `#F2B705` avec parcimonie.

## Interdits

Cartes d'Afrique décoratives, motifs folkloriques, dégradés multicolores, photos de
banque d'images présentées comme le chantier réel, logos d'institutions (on écrit leur
nom). Une photo n'est utilisée que si sa source et ses droits sont connus.

## Contrôle

Ouvrir chaque visuel et vérifier : chiffres identiques aux fiches, texte lisible sur
téléphone (corps 28 px au moins), aucune page vide.
