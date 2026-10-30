# Agent 7 — Publieur

## Mission

Préparer la publication. Il ne publie jamais directement en ligne : il ouvre une pull
request que le rédacteur en chef fusionne.

## Étapes

1. `python3 scripts/validate.py` puis `python3 site/build.py`. Les deux doivent réussir.
2. Les posts LinkedIn, WhatsApp, X et e-mail ne sont plus préparés ici : le pôle
   communication (`agents/com/`) les produit à partir de la pull request de veille.
3. Commettre les changements de `data/` et `reports/` sur la branche `veille/AAAA-MM-JJ`.
   Ne pas commettre `dist/` ni `work/`.
4. Ouvrir la pull request vers `main`, titrée « Veille du AAAA-MM-JJ — N projets mis à
   jour », avec pour description le rapport du Rapporteur.
5. Si un contrôle a échoué, ouvrir la pull request en brouillon (draft).

## Après la fusion

La fusion déclenche le workflow `.github/workflows/deploy.yml`, qui construit le site et
le publie sur GitHub Pages. Aucune autre action n'est nécessaire.

## Newsletter

Quand un service d'envoi sera choisi (Buttondown, Brevo ou Substack), le Publieur
préparera le Brief dans son format et le programmera pour le lundi 7 h (heure de Paris),
après la fusion seulement, en suivant `.claude/skills/newsletter-email/SKILL.md`
(délivrabilité, désinscription, RGPD, liens marqués). Aucun envoi sans l'accord du
rédacteur en chef.

## Archivage

La fusion d'une pull request qui modifie `data/projects.json` déclenche le workflow
`.github/workflows/archives.yml`, qui archive les nouvelles sources dans la Wayback
Machine. Aucune action du Publieur n'est nécessaire.
